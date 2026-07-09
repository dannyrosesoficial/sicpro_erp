# -*- coding: utf-8 -*-

import base64
from odoo.modules.module import get_module_resource
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from random import randint
import qrcode
from io import BytesIO
from odoo.exceptions import UserError


class Credenciales(models.Model):
    _name = 'sicpro.app.credenciales'
    _description = "Credenciales de los Trabajadores"
    _order = 'trabajador'
    _inherit = ['mail.activity.mixin', 'mail.thread']

    def _default_color(self):
        return randint(1, 11)

    @api.model
    def _default_image(self):
        image_path = get_module_resource('sicpro_app_credenciales',
                                         'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    name = fields.Char(string="Nombre de trabajador", )
    trabajador = fields.Many2one('sicpro.app.trabajadores', index=True,
                                 required=True, tracking=True,
                                 string="Nombre del trabajador", )
    active = fields.Boolean('Activo', default=True)
    plaza_id = fields.Char(string="# Plaza", related='trabajador.plaza_id',
                           store=True)
    telefono_trabajo = fields.Char('Teléfono Trabajo',
                                   related='trabajador.telefono_trabajo',
                                   store=True)
    movil_trabajo = fields.Char('Móvil Trabajo',
                                related='trabajador.movil_trabajo', store=True)
    correo_trabajo = fields.Char('Correo Trabajo',
                                 related='trabajador.correo_trabajo',
                                 store=True)

    company_id = fields.Many2one('res.company', string='Proceso',
                                 related='trabajador.company_id', store=True)
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                                   'Puesto de trabajo',
                                   related='trabajador.ocupacion_id',
                                   store=True)
    area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Departamento',
                              related='trabajador.area_id', store=True)
    parent_id = fields.Many2one('sicpro.app.trabajadores', 'Jefe Inmediato',
                                related='trabajador.parent_id', store=True)
    inicio_contrato = fields.Date(string="Inicio del Contrato",
                                  related='trabajador.inicio_contrato',
                                  store=True)
    fecha_incorporacion = fields.Date(string="Fecha de Incorporación",
                                      related='trabajador.fecha_incorporacion',
                                      store=True)
    ubicacion_laboral = fields.Text(string="Ubicación Laboral", store=True,
                                    related='trabajador.ubicacion_laboral')
    fecha_baja = fields.Date('Fecha Baja', related='trabajador.fecha_baja',
                             store=True)
    clase_contrato = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.categorias', store=True,
        string='Clase de Contrato', related='trabajador.clase_contrato')
    categoria_ocupacional = fields.Many2one(
        comodel_name='sicpro.app.trabajadores.categorias', store=True,
        string='Categoría Ocupacional',
        related='trabajador.categoria_ocupacional')
    identification_id = fields.Char(string='Carnet de identidad', store=True,
                                    related='trabajador.identification_id')
    direccion_carnet = fields.Char(string="Dirección CI", store=True,
                                   related='trabajador.direccion_carnet')
    raza = fields.Selection(string="Raza", related='trabajador.raza',
                            store=True)
    genero = fields.Selection(string="Género", default="masculino",
                              related='trabajador.genero', store=True)
    fecha_nacimiento = fields.Date('Fecha de nacimiento', store=True,
                                   related='trabajador.fecha_nacimiento')
    user_id = fields.Many2one('res.users', 'Usuario SICPRO ERP',
                              related='trabajador.user_id', store=True)
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())

    credencial_image_1920 = fields.Image("Image", max_width=1920,
                                         max_height=1920,
                                         default=_default_image)
    # campos redimensionados almacenados (como adjunto) para rendimiento
    credencial_image_1024 = fields.Image("Image 1024",
                                         related="credencial_image_1920",
                                         max_width=1024, max_height=1024,
                                         store=True)
    credencial_image_512 = fields.Image("Image 512",
                                        related="credencial_image_1920",
                                        max_width=512, max_height=512,
                                        store=True)
    credencial_image_256 = fields.Image("Image 256",
                                        related="credencial_image_1920",
                                        max_width=256, max_height=256,
                                        store=True)
    credencial_image_128 = fields.Image("Image 128",
                                        related="credencial_image_1920",
                                        max_width=128, max_height=128,
                                        store=True)
    no_credencial = fields.Char(string='No. Credencial', copy=False,
                                readonly=True, )
    Usuario = fields.Many2one(comodel_name='res.users',
                              string='Usuario Registro', index=True,
                              default=lambda self: self.env.uid)
    fecha_actual = fields.Date(string='Fecha Registro',
                               default=lambda self: fields.Date.context_today(self))
    fecha_entrega = fields.Date(string='Fecha Entrega', required=True)
    fecha_valida = fields.Date(string='Valida hasta',
                               compute='_compute_fecha_valida', store=True)
    tiene_laptop = fields.Boolean(string='Tiene_laptop', required=False)
    laptop_no_serie = fields.Char(string='No. Serie', required=False)
    laptop_no_folio = fields.Char(string='No. Folio', required=False)
    laptop_no_inventario = fields.Char(string='No. Inventario', required=False)
    laptop_image_1920 = fields.Image("Imagen Laptop", max_width=1920,
                                     max_height=1920, )
    laptop_image_256 = fields.Image("Img 256", related="laptop_image_1920",
                                    max_width=256, max_height=256, store=True)
    tipo_credencial = fields.Many2one(
        comodel_name='sicpro.app.credenciales.tipo', string='Tipo',
        required=True)
    siglas_credencial = fields.Many2one(
        comodel_name='sicpro.app.credenciales.siglas', string='Siglas',
        required=True)
    alcance_credencial = fields.Many2one(
        comodel_name='sicpro.app.credenciales.alcance', string='Alcance',
        required=True)
    accesos_credencial = fields.Many2one(
        comodel_name='sicpro.app.credenciales.accesos', string='Accesos',
        required=True)
    correo_seguidores = fields.Char(string="correo_seguidores", index=True)
    qr_code = fields.Binary("Código QR", required=False)

    def generate_qr(self):
        if self.name:
            if self.ocupacion_id:
                qr = qrcode.QRCode(version=1,
                                   error_correction=qrcode.constants.ERROR_CORRECT_L,
                                   box_size=10, border=4, )


                qr.add_data('Credencial: ' + self.no_credencial)
                qr.add_data('\n')
                qr.add_data(self.name)
                qr.add_data('\n')
                qr.add_data(self.ocupacion_id.name.name)
                qr.add_data('\n')
                qr.add_data('Plaza: ' + self.plaza_id)
                qr.add_data('\n')
                qr.add_data(self.company_id.name)
                qr.make(fit=True)
                img = qr.make_image()
                tmp = BytesIO()
                img.save(tmp, format="PNG")
                qr_img = base64.b64encode(tmp.getvalue())
                self.qr_code = qr_img
            else:
                raise UserError(
                    _('Chequear el nombre del trabajador y la ocupación'))

    # calcula el tiempo de validez del pase o credencial
    @api.depends('fecha_entrega')
    def _compute_fecha_valida(self):
        if self.fecha_entrega:
            self.fecha_valida = self.fecha_entrega + relativedelta(days=365)

    @api.onchange('trabajador')
    def _onchange_trabajador(self):
        if self.trabajador:
            self.name = self.trabajador.name
        else:
            self.name = None

    def desactivar_trabajador(self):
        control = fields.Datetime.now()
        data = self.env['sicpro.app.credenciales'].search(
            [('fecha_valida', '=', control)])

        for item in data:
            item.active = False
            # envió la notificación a los seguidores
            data.message_post(body='Usuario' + item.name + 'vencido',
                              message_type='notification',
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # mantiene actualizado el correo de seguidores del registro
            correos = ''
            for follower in data.message_partner_ids:
                correos = str(correos) + str(follower.email_formatted)
            data.correo_seguidores = correos
            # envío el correo a los seguidores del registro
            local_context = data.env.context.copy()
            template = data.env.ref(
                'sicpro_app_credenciales.credenciales_usuario_desactivado')
            template.with_context(local_context).send_mail(data.id,
                                                           force_send=True)

    @api.model
    def create(self, vals):
        res = super(Credenciales, self).create(vals)
        # Crear la secuencia de incremento para el consecutivo del proveedor
        res['no_credencial'] = self.env['ir.sequence'].next_by_code(
            'credencial_consecutivo_incrementar')
        res.generate_qr()
        return res

    _sql_constraints = [
        ('name_uniq', 'unique (trabajador)', "El nombre del trabajador existe!, verifiquelo"), ]
