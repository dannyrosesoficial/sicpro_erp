# -*- coding: utf-8 -*-

import base64
from odoo.modules.module import get_module_resource
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from random import randint
import qrcode
from io import BytesIO
from odoo.exceptions import UserError
import datetime
from datetime import datetime, date
import json


def _default_color():
    return randint(1, 11)


class Credenciales(models.Model):
    _name = 'sicpro.app.credenciales'
    _description = "Credenciales de los Trabajadores"
    _order = 'trabajador'
    _inherit = ['mail.activity.mixin', 'mail.thread']

    @api.model
    def imagen_por_defecto(self):
        image_path = get_module_resource('sicpro_app_credenciales', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    @api.model
    def _default_image(self):
        image_path = get_module_resource('sicpro_app_credenciales', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string="Nombre de trabajador", )
    # Nombre sin segundos nombres, para hacer los pases
    name_corto = fields.Char(string="Nombre corto de trabajador", index=True, required=False)
    dominio_trabajador = fields.Char(compute="_compute_get_trabajadores", readonly=True, store=False, copy=False)
    trabajador = fields.Many2one('sicpro.app.trabajadores', index=True, required=False, tracking=True,
                                 string="Nombre del trabajador", )
    active = fields.Boolean('Activo', default=True)
    plaza_id = fields.Char(string="# Plaza", related='trabajador.plaza_id', store=True)
    telefono_trabajo = fields.Char('Teléfono Trabajo', related='trabajador.telefono_trabajo', store=True)
    movil_trabajo = fields.Char('Móvil Trabajo', related='trabajador.movil_trabajo', store=True)
    correo_trabajo = fields.Char('Correo Trabajo', related='trabajador.correo_trabajo', store=True)

    company_id = fields.Many2one('res.company', string='Proceso', related='trabajador.company_id', store=True)
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion', 'Puesto de trabajo',
                                   related='trabajador.ocupacion_id', store=True)
    area_id = fields.Many2one('sicpro.app.trabajadores.areas', 'Departamento', related='trabajador.area_id', store=True)
    parent_id = fields.Many2one('sicpro.app.trabajadores', 'Jefe Inmediato', related='trabajador.parent_id', store=True)
    inicio_contrato = fields.Date(string="Inicio del Contrato", related='trabajador.inicio_contrato', store=True)
    fecha_incorporacion = fields.Date(string="Fecha de Incorporación", related='trabajador.fecha_incorporacion',
                                      store=True)
    ubicacion_laboral = fields.Text(string="Ubicación Laboral", store=True, related='trabajador.ubicacion_laboral')
    fecha_baja = fields.Date('Fecha Baja', related='trabajador.fecha_baja', store=True)
    clase_contrato = fields.Many2one(comodel_name='sicpro.app.trabajadores.categorias', store=True,
                                     string='Clase de Contrato', related='trabajador.clase_contrato')
    categoria_ocupacional = fields.Many2one(comodel_name='sicpro.app.trabajadores.categorias', store=True,
                                            string='Categoría Ocupacional', related='trabajador.categoria_ocupacional')
    identification_id = fields.Char(string='Carnet de identidad', store=True, related='trabajador.identification_id')
    direccion_carnet = fields.Char(string="Dirección CI", store=True, related='trabajador.direccion_carnet')
    raza = fields.Selection(string="Raza", related='trabajador.raza', store=True)
    genero = fields.Selection(string="Género", related='trabajador.genero', store=True)
    fecha_nacimiento = fields.Date('Fecha de nacimiento', store=True, related='trabajador.fecha_nacimiento')
    user_id = fields.Many2one('res.users', 'Usuario SICPRO ERP', related='trabajador.user_id', store=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    credencial_image_1920 = fields.Image("Image", max_width=1920, max_height=1920, default=_default_image)
    # campos redimensionados almacenados (como adjunto) para rendimiento
    credencial_image_1024 = fields.Image("Image 1024", related="credencial_image_1920", max_width=1024, max_height=1024,
                                         store=False)
    credencial_image_512 = fields.Image("Image 512", related="credencial_image_1920", max_width=512, max_height=512,
                                        store=False)
    credencial_image_256 = fields.Image("Image 256", related="credencial_image_1920", max_width=256, max_height=256,
                                        store=False)
    credencial_image_128 = fields.Image("Image 128", related="credencial_image_1920", max_width=128, max_height=128,
                                        store=False)
    no_credencial_permanente = fields.Char(string='No. Credencial Permanente', copy=False, readonly=False, )
    no_credencial_laptop = fields.Char(string='No. Credencial Laptop', copy=False, readonly=False, )
    no_credencial_provisional = fields.Char(string='No. Credencial Provisional', copy=False, readonly=False, )
    no_credencial_constructores = fields.Char(string='No. Credencial Constructores', copy=False, readonly=False, )
    no_credencial_especial = fields.Char(string='No. Credencial Especial', copy=False, readonly=False, )
    usuario = fields.Many2one(comodel_name='res.users', string='Usuario Registro', index=True,
                              default=lambda self: self.env.uid)
    fecha_actual = fields.Date(string='Fecha Registro', default=lambda self: fields.Date.context_today(self))
    fecha_entrega = fields.Date(string='Fecha Entrega', required=False)
    fecha_valida = fields.Date(string='Válida hasta', compute='_compute_fecha_valida', store=True)
    tiene_laptop = fields.Boolean(string='Tiene_laptop', required=False)
    laptop_no_serie = fields.Char(string='No. Serie', required=False)
    laptop_no_folio = fields.Char(string='No. Folio', required=False)
    laptop_no_inventario = fields.Char(string='No. Inventario', required=False)
    laptop_image_1920 = fields.Image("Imagen Laptop", max_width=1920, max_height=1920, )
    laptop_image_256 = fields.Image("Img 256", related="laptop_image_1920", max_width=256, max_height=256, store=True)
    tipo_credencial = fields.Many2one(comodel_name='sicpro.app.credenciales.tipo', string='Tipo', required=True)
    personal_externo = fields.Boolean(string='Personal Externo', related="tipo_credencial.personal_externo")
    observaciones = fields.Text(string="Observaciones")
    cancelacion_motivos = fields.Many2one(comodel_name='sicpro.app.credenciales.cancelacion',
                                          string='Motivos de la Cancelación', required=False)
    cancelacion_fecha = fields.Date(string='Fecha Cancelación', required=False)
    cancelacion_active = fields.Boolean(string='Cancelacion_active', default=False, required=False)

    especial_telefono_trabajo = fields.Char('Teléfono Trabajo (Esp.)')
    especial_movil_trabajo = fields.Char('Móvil Trabajo (Esp.)')
    especial_correo_trabajo = fields.Char('Correo Trabajo (Esp.)')
    especial_company_id = fields.Char(string='Proceso (Esp.)')
    especial_ocupacion_id = fields.Char('Puesto de trabajo (Esp.)')
    especial_area_id = fields.Char('Departamento (Esp.)')
    especial_inicio_contrato = fields.Date(string="Inicio del Contrato (Esp.)")
    especial_fecha_incorporacion = fields.Date(string="Fecha de Incorporación (Esp.)")
    especial_ubicacion_laboral = fields.Text(string="Ubicación Laboral (Esp.)")
    especial_fecha_baja = fields.Date('Fecha Baja (Esp.)')
    especial_identification_id = fields.Char(string='Carnet de identidad (Esp.)')
    especial_direccion_carnet = fields.Char(string="Dirección CI (Esp.)")
    especial_raza = fields.Selection([('blanca', 'Blanca'), ('mestiza', 'Mestiza'), ('negra', 'Negra')],
                                     string="Raza (Esp.)", tracking=True)
    especial_genero = fields.Selection([('masculino', 'Masculino'), ('femenino', 'Femenino'), ], string="Género (Esp.)",
                                       tracking=True)

    # Campo para obtener el nombre del tipo de credencial seleccionado, para mostrar u ocultar campos
    # según el tipo de credencial
    nombre_credencial = fields.Char(string='Nombre de la Credencial', related='tipo_credencial.name')
    siglas_credencial = fields.Many2one(comodel_name='sicpro.app.credenciales.siglas', string='Siglas', required=True)
    alcance_credencial = fields.Many2one(comodel_name='sicpro.app.credenciales.alcance', string='Alcance',
                                         required=True)
    accesos_credencial = fields.Many2one(comodel_name='sicpro.app.credenciales.accesos', string='Accesos',
                                         required=True, )
    qr_code = fields.Binary("Código QR", required=False)

    @api.model
    @api.depends('trabajador')
    def _compute_get_trabajadores(self):
        dic = []
        credenciales = self.env['sicpro.app.credenciales'].sudo().search([('active', '=', True)])
        if credenciales:
            for value in credenciales:
                dic.append(value.trabajador.id)
        self.dominio_trabajador = json.dumps([('id', 'not in', dic)])

    def generate_qr(self):
        if self.name:
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, )

            # Añadir el número de credencial según el tipo de credencial
            if 'PERMANENTE' in self.tipo_credencial.name:
                qr.add_data('Credencial: ' + self.no_credencial_permanente)
            elif 'CONSTRUCTOR' in self.tipo_credencial.name:
                qr.add_data('Credencial: ' + self.no_credencial_constructores)
            elif 'ESPECIAL' in self.tipo_credencial.name:
                qr.add_data('Credencial: ' + self.no_credencial_especial)
            else:
                qr.add_data('Credencial: ' + self.no_credencial_provisional)

            qr.add_data('\n')
            qr.add_data(self.name)
            qr.add_data('\n')
            if not self.personal_externo:
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
            raise UserError(_('Chequear el nombre del trabajador'))

    # abrir modal para recortar imagen (con el botón invisible)
    def abrir_modal_recortar_imagen(self):
        return {'type': 'ir.actions.act_window', 'name': 'Recortar Imagen',
                'res_model': 'sicpro.app.credenciales.modal', 'view_mode': 'form', 'target': 'new', }

    # calcula el tiempo de validez del pase o credencial
    @api.depends('fecha_entrega', 'tipo_credencial')
    def _compute_fecha_valida(self):
        if self.fecha_entrega and 'PERMANENTE' not in self.tipo_credencial.name and 'CONSTRUCTOR' not in self.tipo_credencial.name:
            self.fecha_valida = datetime(month=12, day=31, year=self.fecha_entrega.year)
        else:
            self.fecha_valida = None

    # Crear nombre corto para los reportes
    @api.onchange('name')
    def _onchange_nombre_corto(self):
        if self.name:
            nombre_corto_final = self.name
            cant_espacios_en_nombre = self.name.count(" ")
            if cant_espacios_en_nombre >= 3:
                segundo_nombre = self.name.partition(' ')[2].partition(' ')[0]
                nombre_corto_final = nombre_corto_final.replace(segundo_nombre, "", 1)
                if cant_espacios_en_nombre >= 4:
                    tercer_nombre = self.name.partition(' ')[2].partition(' ')[2].partition(' ')[0]
                    nombre_corto_final = nombre_corto_final.replace(tercer_nombre, "", 1)
                if cant_espacios_en_nombre >= 5:
                    cuarto_nombre = self.name.partition(' ')[2].partition(' ')[2].partition(' ')[2].partition(' ')[0]
                    nombre_corto_final = nombre_corto_final.replace(cuarto_nombre, "", 1)

            self.name_corto = nombre_corto_final

    # Cambiar la foto del trabajador y el usuario cuando se selecciona o se elimina una nueva imagen
    @api.onchange('credencial_image_1920')
    def _onchange_foto_trabajador(self):
        if self.credencial_image_1920:
            if self.trabajador:
                self.trabajador.sudo().image_1920 = self.credencial_image_1920
                if self.trabajador.user_id:
                    self.trabajador.sudo().user_id.image_1920 = self.credencial_image_1920
        else:
            if self.trabajador:
                self.trabajador.sudo().image_1920 = None
                if self.trabajador.user_id:
                    self.trabajador.sudo().user_id.image_1920 = None

    @api.onchange('trabajador')
    def _onchange_trabajador(self):
        if self.trabajador:
            self.name = self.trabajador.name
            if 'Indeterminado' in self.trabajador.clase_contrato.name:
                self.tipo_credencial = self.env['sicpro.app.credenciales.tipo'].search([('name', 'like', 'PERMANENTE')])
            elif 'Determinado' in self.trabajador.clase_contrato.name:
                self.tipo_credencial = self.env['sicpro.app.credenciales.tipo'].search(
                    [('name', 'like', 'PROVISIONAL')])
        else:
            self.name = None

    def desactivar_trabajador(self):
        control = fields.Datetime.now()
        data = self.env['sicpro.app.credenciales'].search([('fecha_valida', '<=', control)])

        for item in data:
            item.active = False
            # envió la notificación a los seguidores
            item.message_post(body='Usuario' + item.name + 'vencido', message_type='notification',
                              subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)

            # Selecciono el registro de seguidores
            for participante in item.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = item.env.context.copy()
                template = self.env.ref('sicpro_app_credenciales.credenciales_usuario_desactivado')
                template.with_context(local_context).send_mail(item.id, force_send=True, email_values=email_values)

    def action_reactiva_trabajador(self):
        self.cancelacion_motivos = None
        self.cancelacion_fecha = ''
        self.cancelacion_active = False
        self.active = True

    @api.model
    def create(self, vals):
        res = super(Credenciales, self).create(vals)
        # Crear la secuencia de incremento para el consecutivo según el tipo de credencial
        if 'PERMANENTE' in res['tipo_credencial'].name:
            res['no_credencial_permanente'] = self.env['ir.sequence'].next_by_code(
                'credencial_permanente_consecutivo_incrementar')
        elif 'CONSTRUCTOR' in res['tipo_credencial'].name:
            res['no_credencial_constructores'] = self.env['ir.sequence'].next_by_code(
                'credencial_constructores_consecutivo_incrementar')
        elif 'ESPECIAL' in res['tipo_credencial'].name:
            res['no_credencial_especial'] = self.env['ir.sequence'].next_by_code(
                'credencial_especial_consecutivo_incrementar')
        else:
            res['no_credencial_provisional'] = self.env['ir.sequence'].next_by_code(
                'credencial_provisional_consecutivo_incrementar')

        if res['tiene_laptop']:
            res['no_credencial_laptop'] = self.env['ir.sequence'].next_by_code(
                'credencial_laptop_consecutivo_incrementar')

        res.generate_qr()
        return res

    def update(self, vals):
        # Para que al renderizar la imagen se vea el cambio se pasan a vals todas las resoluciones de imágenes
        if 'credencial_image_1920' in vals:
            vals['credencial_image_1024'] = vals['credencial_image_1920']
            vals['credencial_image_512'] = vals['credencial_image_1920']
            vals['credencial_image_256'] = vals['credencial_image_1920']
            vals['credencial_image_128'] = vals['credencial_image_1920']

        # Crear la secuencia de incremento para el consecutivo
        # según el tipo de credencial
        if 'tipo_credencial' in vals:
            nombre_credencial_temp = self.env['sicpro.app.credenciales.tipo'].browse(vals['tipo_credencial']).name
            if 'PERMANENTE' in nombre_credencial_temp and not self.no_credencial_permanente:
                vals['no_credencial_permanente'] = self.env['ir.sequence'].next_by_code(
                    'credencial_permanente_consecutivo_incrementar')
            elif 'CONSTRUCTOR' in nombre_credencial_temp and not self.no_credencial_constructores:
                vals['no_credencial_constructores'] = self.env['ir.sequence'].next_by_code(
                    'credencial_constructores_consecutivo_incrementar')
            elif 'ESPECIAL' in nombre_credencial_temp and not self.no_credencial_especial:
                vals['no_credencial_especial'] = self.env['ir.sequence'].next_by_code(
                    'credencial_especial_consecutivo_incrementar')
            elif 'PROVISIONAL' in nombre_credencial_temp and not self.no_credencial_provisional:
                vals['no_credencial_provisional'] = self.env['ir.sequence'].next_by_code(
                    'credencial_provisional_consecutivo_incrementar')

        res = super(Credenciales, self).update(vals)

        # Actualizar Imagen de trabajadores y usuarios
        # (Actualizar las imágenes para que se renderice correctamente)
        if 'credencial_image_1920' in vals:
            if self.credencial_image_1920:
                if self.trabajador:
                    self.trabajador.image_1920 = self.credencial_image_1920
                    if self.trabajador.user_id:
                        self.trabajador.user_id.image_1920 = self.credencial_image_1920
            else:
                if self.trabajador:
                    self.trabajador.image_1920 = None
                    if self.trabajador.user_id:
                        self.trabajador.user_id.image_1920 = None

        return res

    # En caso de que se quiera usar write en lugar de update para actualizar registros
    def write(self, vals):
        # Para que al renderizar la imagen se vea el cambio se pasan a vals todas las resoluciones de imágenes
        if 'credencial_image_1920' in vals:
            vals['credencial_image_1024'] = vals['credencial_image_1920']
            vals['credencial_image_512'] = vals['credencial_image_1920']
            vals['credencial_image_256'] = vals['credencial_image_1920']
            vals['credencial_image_128'] = vals['credencial_image_1920']

        # Crear la secuencia de incremento para el consecutivo según el tipo de credencial
        if 'tipo_credencial' in vals:
            nombre_credencial_temp = self.env['sicpro.app.credenciales.tipo'].browse(vals['tipo_credencial']).name
            if 'PERMANENTE' in nombre_credencial_temp and not self.no_credencial_permanente:
                vals['no_credencial_permanente'] = self.env['ir.sequence'].next_by_code(
                    'credencial_permanente_consecutivo_incrementar')
            elif 'CONSTRUCTOR' in nombre_credencial_temp and not self.no_credencial_constructores:
                vals['no_credencial_constructores'] = self.env['ir.sequence'].next_by_code(
                    'credencial_constructores_consecutivo_incrementar')
            elif 'ESPECIAL' in nombre_credencial_temp and not self.no_credencial_especial:
                vals['no_credencial_especial'] = self.env['ir.sequence'].next_by_code(
                    'credencial_especial_consecutivo_incrementar')
            elif 'PROVISIONAL' in nombre_credencial_temp and not self.no_credencial_provisional:
                vals['no_credencial_provisional'] = self.env['ir.sequence'].next_by_code(
                    'credencial_provisional_consecutivo_incrementar')

        if 'tiene_laptop' in vals:
            if vals['tiene_laptop'] and not self.no_credencial_laptop:
                vals['no_credencial_laptop'] = self.env['ir.sequence'].next_by_code(
                    'credencial_laptop_consecutivo_incrementar')

        res = super(Credenciales, self).write(vals)

        # Actualizar Imagen de trabajadores y usuarios (Actualizar las imágenes para que se renderice correctamente)
        if 'credencial_image_1920' in vals:
            if self.credencial_image_1920:
                if self.trabajador:
                    self.trabajador.sudo().image_1920 = self.credencial_image_1920
                    if self.trabajador.user_id:
                        self.trabajador.sudo().user_id.image_1920 = self.credencial_image_1920
            else:
                if self.trabajador:
                    self.trabajador.sudo().image_1920 = None
                    if self.trabajador.user_id:
                        self.trabajador.sudo().user_id.image_1920 = None

        return res

    _sql_constraints = [('name_uniq', 'unique (trabajador)', "El nombre del trabajador existe!, verifíquelo"), ]


# cancelar usuario
class CredencialesCancelarTrabajadores(models.TransientModel):
    _name = 'sicpro.app.credenciales.cancelar'
    _description = 'Cancelar Trabajadores'

    motivo_cancelacion = fields.Many2one(comodel_name='sicpro.app.credenciales.cancelacion',
                                         string='Motivos de la Cancelación', required=True)

    def action_motivo_cancelacion(self):
        # cambio el estado interno de la credencial
        credencial = self.env['sicpro.app.credenciales'].browse(self.env.context.get('active_ids'))
        for item in credencial:
            item.cancelacion_motivos = self.motivo_cancelacion
            item.cancelacion_fecha = fields.Date.context_today(self)
            item.cancelacion_active = True
            item.active = False

        # redirecciono la salida
        action = self.env.ref('sicpro_app_credenciales.credenciales_views_actions').sudo().read()[0]
        return action
