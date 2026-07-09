# -*- coding: utf-8 -*-

import base64
import hashlib
import io
import math
import logging
import mimetypes
import os
import re
from collections import defaultdict
from PIL import Image
from odoo import api, fields, models, tools, _
from odoo.exceptions import AccessError, UserError
from odoo.tools import human_size, ImageProcess, str2bool
from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)


class SalonClasesAdjuntos(models.Model):
    _name = 'sicpro.app.salon.clases.adjuntos'
    _description = 'Documentación del Salón de Clases'
    _order = 'id desc'


    @api.model
    def _directorio(self):
        return 'file'

    @api.model
    def _directorio_archivos(self):
        directorio = self.env['ir.config_parameter'].sudo().get_param(
            'sicpro_app_salon_clases.directorio')
        return directorio

    @api.model
    def _directorio_completo(self, path):
        # despejar camino
        path = re.sub('[.]', '', path)
        path = path.strip('/\\')
        return os.path.join(self._directorio_archivos(), path)

    @api.model
    def _buscar_directorio(self, bin_data, sha):
        # retrocompatibilidad
        fname = sha[:3] + '/' + sha
        full_path = self._directorio_completo(fname)
        if os.path.isfile(full_path):
            return fname, full_path

        # archivos dispersos en 256 directorios
        # usamos '/' en la base de datos (incluso en Windows)
        fname = sha[:2] + '/' + sha
        full_path = self._directorio_completo(fname)
        dirname = os.path.dirname(full_path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        # prevenir la colisión sha-1
        if os.path.isfile(full_path) and not self._same_content(bin_data, full_path):
            raise UserError("El archivo adjunto está en conflicto con un archivo existente.")
        return fname, full_path

    @api.model
    def _leer_archivo(self, fname):
        full_path = self._directorio_completo(fname)
        try:
            with open(full_path, 'rb') as f:
                return f.read()
        except (IOError, OSError):
            _logger.info("_read_file reading %s", full_path, exc_info=True)
        return b''

    @api.model
    def _escribir_archivo(self, bin_value, checksum):
        fname, full_path = self._buscar_directorio(bin_value, checksum)
        if not os.path.exists(full_path):
            try:
                with open(full_path, 'wb') as fp:
                    fp.write(bin_value)
                # agregue fname a la lista de verificación, en caso de que
                # la transacción se anule
                self._mark_for_gc(fname)
            except IOError:
                _logger.info("_escribir_archivo escribiendo %s", full_path, exc_info=True)
        return fname

    @api.model
    def _eliminar_archivo(self, fname):
        # simplemente agregue fname a la lista de verificación, se
        # recolectará como basura más tarde
        self._mark_for_gc(fname)

    def _mark_for_gc(self, fname):
        """ Agregue ``fname`` en una lista de verificación para la recolección
        de basura del almacén de archivos. """
        # usamos un spooldir: agregue un archivo vacío en el subdirectorio
        # 'lista de verificación'
        full_path = os.path.join(self._directorio_completo('checklist'), fname)
        if not os.path.exists(full_path):
            dirname = os.path.dirname(full_path)
            if not os.path.isdir(dirname):
                with tools.ignore(OSError):
                    os.makedirs(dirname)
            open(full_path, 'ab').close()

    # cron de limpieza del directorio de los documentos
    # @api.autovacuum
    def cron_salon_cleaner(self):
        """ Realice la recolección de elementos no utilizados del
        almacén de archivos. """
        if self._directorio() != 'file':
            return

        cr = self._cr
        cr.commit()

        # evitar todas las actualizaciones simultáneas en
        # sicpro_app_salon_clases_adjuntos
        cr.execute("SET LOCAL lock_timeout TO '10s'")
        cr.execute("LOCK sicpro_app_salon_clases_adjuntos IN SHARE MODE")

        # recuperar los nombres de archivo de la lista de verificación
        checklist = {}
        for dirpath, _, filenames in os.walk(self._directorio_completo('checklist')):
            dirname = os.path.basename(dirpath)
            for filename in filenames:
                fname = "%s/%s" % (dirname, filename)
                checklist[fname] = os.path.join(dirpath, filename)

        # Limpiar la lista de verificación. La lista de verificación se divide
        # en partes y los archivos se recolectan como elementos no utilizados.
        # for each chunk.
        removed = 0
        for names in cr.split_for_in_conditions(checklist):
            # determinar qué archivos mantener entre la lista de verificación
            cr.execute("SELECT store_fname FROM sicpro_app_salon_clases_adjuntos WHERE store_fname IN %s", [names])
            whitelist = set(row[0] for row in cr.fetchall())

            # elimine los archivos basura y limpie la lista de verificación
            for fname in names:

                filepath = checklist[fname]
                if fname not in whitelist:
                    try:
                        os.unlink(self._directorio_completo(fname))
                        _logger.debug("_file_gc desvinculado %s", self._directorio_completo(fname))
                        removed += 1
                    except (OSError, IOError):
                        _logger.info("_file_gc no pudo desvincular %s", self._directorio_completo(fname), exc_info=True)
                with tools.ignore(OSError):
                    os.unlink(filepath)

        # comprometerse a liberar el candado
        cr.commit()

        _logger.info("almacén de archivos gc %d verificado, %d eliminado", len(checklist), removed)

    @api.depends('store_fname', 'db_datas', 'file_size')
    @api.depends_context('bin_size')
    def _compute_datas(self):
        if self._context.get('bin_size'):
            for attach in self:
                attach.datas = human_size(attach.file_size)
            return

        for attach in self:
            attach.datas = base64.b64encode(attach.raw or b'')

    @api.depends('store_fname', 'db_datas')
    def _compute_raw(self):
        for attach in self:
            if attach.store_fname:
                attach.raw = attach._leer_archivo(attach.store_fname)
            else:
                attach.raw = attach.db_datas

    def _inverse_raw(self):
        self._set_attachment_data(lambda a: a.raw or b'')

    def _inverse_datas(self):
        self._set_attachment_data(lambda attach: base64.b64decode(attach.datas or b''))

    def _set_attachment_data(self, asbytes):
        for attach in self:
            # calcular los campos que dependen de los datos
            bin_data = asbytes(attach)
            vals = self._get_datas_related_values(bin_data, attach.mimetype)

            # tomar la ubicación actual en el almacén de archivos para
            # posiblemente recolectar basura
            fname = attach.store_fname
            # escribir como superusuario, ya que el usuario probablemente no
            # tiene acceso de escritura
            super(SalonClasesAdjuntos, attach.sudo()).write(vals)
            if fname:
                self._eliminar_archivo(fname)

    def _get_datas_related_values(self, data, mimetype):
        values = {
            'file_size': len(data),
            'checksum': self._compute_checksum(data),
            'index_content': self._index(data, mimetype),
            'store_fname': False,
            'db_datas': data,
        }
        if data and self._directorio() != 'db':
            values['store_fname'] = self._escribir_archivo(data, values['checksum'])
            values['db_datas'] = False
        return values

    def _compute_checksum(self, bin_data):
        """ calcular la suma de comprobación para los datos dados
            :param bin_data : datos en su forma binaria
        """
        # un archivo vacío también tiene una suma de comprobación
        # (para el almacenamiento en caché)
        return hashlib.sha1(bin_data or b'').hexdigest()

    @api.model
    def _same_content(self, bin_data, filepath):
        BLOCK_SIZE = 1024
        with open(filepath, 'rb') as fd:
            i = 0
            while True:
                data = fd.read(BLOCK_SIZE)
                if data != bin_data[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]:
                    return False
                if not data:
                    break
                i += 1
        return True

    # verifica el tipo de archivo
    def _compute_mimetype(self, values):
        mimetype = None
        if values.get('mimetype'):
            mimetype = values['mimetype']
        if not mimetype and values.get('name'):
            mimetype = mimetypes.guess_type(values['name'])[0]
        if not mimetype or mimetype == 'application/octet-stream':
            raw = None
            if values.get('raw'):
                raw = values['raw']
            elif values.get('datas'):
                raw = base64.b64decode(values['datas'])
            if raw:
                mimetype = guess_mimetype(raw)
        return mimetype or 'application/octet-stream'

    # procesa el contenido
    def _postprocess_contents(self, values):
        ICP = self.env['ir.config_parameter'].sudo().get_param
        supported_subtype = ICP('base.image_autoresize_extensions', 'png,jpeg,gif,bmp,tif').split(',')

        mimetype = values['mimetype'] = self._compute_mimetype(values)
        _type, _subtype = mimetype.split('/')
        is_image_resizable = _type == 'image' and _subtype in supported_subtype
        if is_image_resizable and (values.get('datas') or values.get('raw')):
            is_raw = values.get('raw')

            # Can be set to 0 to skip the resize
            max_resolution = ICP('base.image_autoresize_max_px', '1920x1920')
            if str2bool(max_resolution, True):
                try:
                    img = fn_quality = False
                    if is_raw:
                        img = ImageProcess(False, verify_resolution=False)
                        img.image = Image.open(io.BytesIO(values['raw']))
                        img.original_format = (img.image.format or '').upper()
                        fn_quality = img.image_quality
                    else:  # datas
                        img = ImageProcess(values['datas'], verify_resolution=False)
                        fn_quality = img.image_base64

                    w, h = img.image.size
                    nw, nh = map(int, max_resolution.split('x'))
                    if w > nw or h > nh:
                        img.resize(nw, nh)
                        quality = int(ICP('base.image_autoresize_quality', 80))
                        values[is_raw and 'raw' or 'datas'] = fn_quality(quality=quality)
                except UserError as e:
                    _logger.info('Post processing ignored : %s', e)
                    pass
        return values

    # Chequea el tipo de archivo
    def _check_contents(self, values):
        mimetype = values['mimetype'] = self._compute_mimetype(values)
        xml_like = 'ht' in mimetype or ( # hta, html, xhtml, etc.
                'xml' in mimetype and    # other xml (svg, text/xml, etc)
                not 'openxmlformats' in mimetype)  # exception for Office formats
        user = self.env.context.get('binary_field_real_user', self.env.user)
        force_text = (xml_like and (not user._is_system() or
            self.env.context.get('attachments_mime_plainxml')))
        if force_text:
            values['mimetype'] = 'text/plain'
        if not self.env.context.get('image_no_postprocess'):
            values = self._postprocess_contents(values)
        return values

    # indexa el contenido
    @api.model
    def _index(self, bin_data, file_type):
        index_content = False
        if file_type:
            index_content = file_type.split('/')[0]
            if index_content == 'text': # calcular index_content solo para el tipo de texto
                words = re.findall(b"[\x20-\x7E]{4,}", bin_data)
                index_content = b"\n".join(words).decode('ascii')
        return index_content

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    res_model = fields.Char('Resource Model', readonly=True)
    res_field = fields.Char('Resource Field', readonly=True)
    res_id = fields.Many2oneReference('Resource ID', model_field='res_model',
                                      readonly=True)
    public = fields.Boolean('Is public document')
    type = fields.Selection([('url', 'URL'), ('binary', 'File')],
                            string='Type', required=True, default='binary',
                            change_default=True)
    # el campo 'datos' se calcula y puede usar los otros campos a continuación
    raw = fields.Binary(string="File Content (raw)",
                        compute='_compute_raw', inverse='_inverse_raw')
    datas = fields.Binary(string='Archivo (base64)',
                          compute='_compute_datas', inverse='_inverse_datas')
    db_datas = fields.Binary('Database Data', attachment=False)
    store_fname = fields.Char('Directorio')
    file_size = fields.Integer('Tamaño del Archivo', readonly=True)
    checksum = fields.Char("Checksum/SHA1", size=40, index=True, readonly=True)
    mimetype = fields.Char('Tipo', readonly=True)
    index_content = fields.Text('Indexed Content', readonly=True, prefetch=False)
    size = fields.Char("Tamaño de Archivo", compute="_compute_convert_size",
                       store=True)

    @api.depends("file_size")
    def _compute_convert_size(self):
        for rec in self:
            if rec.file_size == 0:
                return "0B"
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(rec.file_size, 1024)))
            p = math.pow(1024, i)
            s = round(rec.file_size / p, 2)
            rec.size = "%s %s" % (s, size_name[i])

    @api.model
    def check(self, mode, values=None):
        if self.env.is_superuser():
            return True
        if not (self.env.is_admin() or self.env.user.has_group(
                'base.group_user')):
            raise AccessError(
                _("Sorry, you are not allowed to access this document."))
        model_ids = defaultdict(set)
        if self:
            self.env['sicpro.app.salon.clases.adjuntos'].flush(
                ['res_model', 'res_id', 'create_uid', 'public', 'res_field'])
            self._cr.execute(
                'SELECT res_model, res_id, create_uid, public, res_field FROM sicpro_app_salon_clases_adjuntos WHERE id IN %s',
                [tuple(self.ids)])
            for res_model, res_id, create_uid, public, res_field in self._cr.fetchall():
                if not self.env.is_system() and res_field:
                    raise AccessError(
                        _("Sorry, you are not allowed to access this document."))
                if public and mode == 'read':
                    continue
                if not (res_model and res_id):
                    continue
                model_ids[res_model].add(res_id)
        if values and values.get('res_model') and values.get('res_id'):
            model_ids[values['res_model']].add(values['res_id'])

        for res_model, res_ids in model_ids.items():
            if res_model not in self.env:
                continue
            if res_model == 'res.users' and len(
                    res_ids) == 1 and self.env.uid == list(res_ids)[0]:
                continue
            records = self.env[res_model].browse(res_ids).exists()
            access_mode = 'write' if mode in ('create', 'unlink') else mode
            records.check_access_rights(access_mode)
            records.check_access_rule(access_mode)

    @api.model_create_multi
    def create(self, vals_list):
        record_tuple_set = set()
        for values in vals_list:
            # remove computed field depending of datas
            for field in ('file_size', 'checksum'):
                values.pop(field, False)
            values = self._check_contents(values)
            raw, datas = values.pop('raw', None), values.pop('datas', None)
            if raw or datas:
                if isinstance(raw, str):
                    # b64decode maneja la entrada str pero raw necesita
                    # una codificación explícita
                    raw = raw.encode()
                values.update(self._get_datas_related_values(
                    raw or base64.b64decode(datas or b''),
                    values['mimetype']
                ))


        return super(SalonClasesAdjuntos, self).create(vals_list)

    def _read(self, fields):
        self.check('read')
        return super(SalonClasesAdjuntos, self)._read(fields)

    def write(self, vals):
        self.check('write', values=vals)
        # remove computed field depending of datas
        for field in ('file_size', 'checksum'):
            vals.pop(field, False)
        if 'mimetype' in vals or 'datas' in vals or 'raw' in vals:
            vals = self._check_contents(vals)
        return super(SalonClasesAdjuntos, self).write(vals)

    def copy(self, default=None):
        self.check('write')
        return super(SalonClasesAdjuntos, self).copy(default)

    def unlink(self):
        if not self:
            return True
        self.check('unlink')
        to_delete = set(attach.store_fname for attach in self if attach.store_fname)
        res = super(SalonClasesAdjuntos, self).unlink()
        for file_path in to_delete:
            self._file_delete(file_path)

        return res

    def _post_add_create(self):
        pass