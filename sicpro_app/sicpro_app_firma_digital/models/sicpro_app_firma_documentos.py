# -*- coding: utf-8 -*-


import base64
import ctypes
import io
import math
import os.path
from random import randint

import PIL.Image
import PyPDF2
import pypdfium2.raw as pdfium_c

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import config


def _default_color():
    return randint(1, 11)


class FirmaDigitalDocumentos(models.Model):
    _name = 'sicpro.app.firma.documentos'
    _description = 'Firmar documentos digitalmente '
    _inherit = ['mail.thread', 'mail.activity.mixin', 'mail.render.mixin']
    _order = 'id desc'

    name = fields.Char('Nombre', required=True)
    pdf_original = fields.Many2many('ir.attachment', string="PDF Original")
    pdf_original_viewer = fields.Binary('Visualizar PDF Original', related='pdf_original.datas')
    pdf_firmado = fields.Many2one('ir.attachment', string="PDF Firmado")
    pdf_firmado_id = fields.Char('id PDF Firmado', compute='_compute_pdf_firmado_idstr')
    pdf_firmado_viewer = fields.Binary('Visualizar PDF Firmado', related='pdf_firmado.datas')
    firma_digital = fields.Binary(string="Firma Digital", )
    estados = fields.Selection(
        [('borrador', 'Borrador'), ('preparacion', 'Preparación'), ('gestion_firma', 'Gestión de Firma'),
         ('rechazado', 'Rechazado'), ('firmado', 'Firmado')], string='Estados', required=True, tracking=True,
        copy=False, default='borrador', group_expand='_group_expand_states')
    etiquetas = fields.Many2many('sicpro.app.firma.etiquetas', 'sicpro_app_firma_etiquetas_rel', string='Etiqueta')
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    user_id = fields.Many2one('res.users', string='Responsable', tracking=True, default=lambda self: self.env.user)
    active = fields.Boolean(default=True)
    fecha_firmado = fields.Datetime(string='Fecha Firmado', copy=False)
    pdf_num_paginas = fields.Integer(string='Num_paginas')
    doc_imagenes_ids = fields.One2many(comodel_name='sicpro.app.firma.documentos.imagenes', inverse_name='name',
                                       string='Imágenes', required=False)
    favorito = fields.Boolean(string='Favorito', required=False, default=False)
    tipo_peticion = fields.Selection(string='Tipo de Petición', required=True, default='simple',
                                     selection=[('simple', 'Único Usuario'), ('multiple', 'Multiples Usuarios'), ], )
    usuario_responsable_firma = fields.Boolean(string='Usuario_responsable_firma', required=False, default=True)
    peticiones_usuarios_ids = fields.Many2many('res.users', 'firma_digital_res_users_rel',
                                               string='Peticiones de Usuarios')
    peticiones_cumplidas_ids = fields.Many2many('res.users', 'firma_digital_res_users_rel',
                                                string='Peticiones de Cumplidas')
    peticiones_user_actual = fields.Many2one('res.users', string='Peticiones de Actual')
    count_peticiones_pendientes = fields.Integer(string="Cantidad de peticiones", compute='_compute_peticiones_count')
    count_peticiones_cumplidas = fields.Integer(string="Cantidad de peticiones", compute='_compute_peticiones_count')

    # Cuenta la cantidad de peticiones pendientes y cumplidas
    def _compute_peticiones_count(self):
        for item in self:
            val1 = item.peticiones_usuarios_ids
            val2 = item.peticiones_cumplidas_ids


    # busco el, id del documento firmado y lo convierto en texto para ser utilizado por javascript
    def _compute_pdf_firmado_idstr(self):
        for item in self:
            if item.pdf_firmado:
                item.pdf_firmado_id = str(item.pdf_firmado.id)
            else:
                item.pdf_firmado_id = None

    # controlar que solo se suba un documento al sistema
    @api.constrains('pdf_original')
    def _check_pdf_original_unico(self):
        contador = 0
        for item in self.pdf_original:
            contador += 1
        if contador > 1:
            raise ValidationError(_("¡Solo debe existir un documento adjunto, si tiene más de uno elimínalo y vuelvalo!"
                                    " a intentar!. Si cree que es un error contacte al administrador"))

    def _group_expand_states(self, states, domain, order):
        return [key for key, val in type(self).estados.selection]

    # busco la cantidad de paginas del documento pdf
    def buscar_paginas_pdf(self):
        if self.pdf_original_viewer:
            data = base64.b64decode(self.pdf_original_viewer)
            if data.startswith(b'%PDF-'):
                pdf = PyPDF2.PdfFileReader(io.BytesIO(data), overwriteWarnings=False, strict=False)
                pdf.getNumPages()
                num_paginas = pdf.numPages
                return num_paginas

    # crear nuevo registro de imagen y de filestore
    def crear_registro_imagenes(self, doc_did, contador, img):
        # salvando archivo en buffer
        buffered = io.BytesIO()
        img.save(buffered, format="png")
        # creo nuevo registro de imagen
        self.env['sicpro.app.firma.documentos.imagenes'].create(
            {'name': doc_did, 'doc_imagen': base64.b64encode(buffered.getvalue()), 'doc_num_page': contador})

    # convierto el pdf en imágenes y pas guardo en la base de datos
    @api.model_create_multi
    def convertir_pdf_imagen(self, paginas):
        # Creo la ruta del documento del data/filestore
        store_fname = str(self.pdf_original.store_fname)
        direct = str(config['data_dir']) + str('/filestore/') + str(self.env.cr.dbname) + str('/')
        directorio_final = direct + store_fname
        # Cargar el documento
        filepath = os.path.abspath(directorio_final)
        pdf = pdfium_c.FPDF_LoadDocument((filepath + "\x00").encode("utf-8"), None)
        # valor por el que se multiplica para hacer más nítida la imagen
        escala = 1
        contador = 0
        while contador < paginas:
            # Cargue la primera página y obtenga sus dimensiones.
            page = pdfium_c.FPDF_LoadPage(pdf, contador)
            width = math.ceil(pdfium_c.FPDF_GetPageWidthF(page)) * escala
            height = math.ceil(pdfium_c.FPDF_GetPageHeightF(page)) * escala
            # Crear un mapa de bits
            use_alpha = False  # No renderizamos con fondo transparente.
            bitmap = pdfium_c.FPDFBitmap_Create(width, height, int(use_alpha))
            # Rellena todo el mapa de bits con un fondo blanco.
            # El color se da como un entero de 32 bits en formato ARGB (8 bits por canal)
            pdfium_c.FPDFBitmap_FillRect(bitmap, 0, 0, width, height, 0xFFFFFFFF)
            # Almacenar argumentos de representación comunes
            render_args = (bitmap,  # el mapa de bits
                           page,  # la página
                           # Las posiciones y los tamaños se darán en píxeles y pueden exceder el mapa de bits.
                           0,  # posición inicial izquierda
                           0,  # posición inicial superior
                           width,  # tamaño horizontal
                           height,  # tamaño vertical
                           0,  # rotación (¡como constante, no en grados!)
                           pdfium_c.FPDF_LCD_TEXT | pdfium_c.FPDF_ANNOT,  # renderizado, combinadas con binario
                           )
            # renderizar la página
            pdfium_c.FPDF_RenderPageBitmap(*render_args)
            # Obtener un puntero al primer elemento del buffer
            first_item = pdfium_c.FPDFBitmap_GetBuffer(bitmap)
            # Reinterpretar el puntero para abarcar todo el búfer
            buffer = ctypes.cast(first_item, ctypes.POINTER(ctypes.c_ubyte * (width * height * 4)))
            # Cree una imagen PIL a partir del contenido del búfer
            img = PIL.Image.frombuffer("RGBA", (width, height), buffer.contents, "raw", "BGRA", 0, 1)
            # Salvar archivo a local deshabilitado
            # img.save("/opt/odoo/sicpro_erp/firma/out_" + str(contador) + ".png")
            # envío los datos para generar los registros de imágenes y del filestore
            doc_id = self._origin.id
            self.crear_registro_imagenes(doc_id, contador, img)
            # Cuento y cierro los recursos
            contador += 1
            pdfium_c.FPDFBitmap_Destroy(bitmap)
            pdfium_c.FPDF_ClosePage(page)
        # Cierro el documento
        pdfium_c.FPDF_CloseDocument(pdf)

    # actualizo registros de imágenes con las dimensiones de cada una
    def actualizar_registro_imagenes_dimensiones(self):
        if self.pdf_original_viewer:
            data = base64.b64decode(self.pdf_original_viewer)
            imagen_ids = self.doc_imagenes_ids
            if data.startswith(b'%PDF-'):
                doc_pdf = PyPDF2.PdfFileReader(io.BytesIO(data), overwriteWarnings=False, strict=False)
                for item in imagen_ids:
                    box = doc_pdf.pages[item.doc_num_page].mediaBox
                    item.doc_ancho = box[2]
                    item.doc_alto = box[3]

    # ejecuto la conversión del pdf a imagen y obtengo los valores de ancho, alto y cantidad de páginas
    def preparar_documento(self):
        if self.pdf_original.ids:
            # cantidad de páginas del documento
            num_paginas = self.buscar_paginas_pdf()
            # guardo la cantidad de páginas
            self.pdf_num_paginas = num_paginas
            # convierto el documento pdf en imagen y lo almaceno
            self.convertir_pdf_imagen(num_paginas)
            # actualizo las dimensiones de las páginas del pdf
            self.actualizar_registro_imagenes_dimensiones()
            # cambio el estado del documento
            self.estados = 'preparacion'
        else:
            raise ValidationError(_("¡Debe adjuntar un documento PDF para comenzar con el proceso de firma!. "
                                    "Si cree que es un error contacte al administrador"))

    # firmar del documento
    def firmar_documento_kanban(self):
        self.ensure_one()
        # llama al wizard
        action = self.sudo().env.ref('sicpro_app_firma_digital.sicpro_app_firma_wizard_action').read()[0]
        return action

    def cancelar_cuadro_firma(self, res_id):
        model = self.env['sicpro.app.firma.documentos'].search([('id', '=', res_id)])
        model.estados = 'preparacion'
        for item in model.doc_imagenes_ids:
            item.doc_crop_izq = 0
            item.doc_crop_der = 0
            item.doc_crop_ancho = 0
            item.doc_crop_alto = 0
            item.doc_firmar = False




    def enviar_documento(self):
        l = 0

    def compartir_documento(self):
        l = 0