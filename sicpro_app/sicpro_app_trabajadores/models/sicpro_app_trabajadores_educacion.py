# -*- coding: utf-8 -*-


from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import pytz

class TrabajadoresEducacion(models.Model):
    _name = 'sicpro.app.trabajadores.educacion'
    _description = "Educación de los trabajadores"
    _order = "line_type_id, date_end desc, date_start desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('sicpro.app.trabajadores', required=True,
                                  ondelete='cascade')
    name = fields.Char(string='Nombre', required=False)
    date_start = fields.Date(string='Fecha inicial', required=True)
    date_end = fields.Date(string='Fecha final', )
    description = fields.Text(string="Descripción")
    line_type_id = fields.Many2one('sicpro.app.trabajadores.educacion.tipos',
                                   string="Tipo de educación")
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Currency', readonly=True,
                                       related='company_id.currency_id')
    pago = fields.Monetary('Pago', related='line_type_id.pago',
                           currency_field='company_currency', store=True)
    display_type = fields.Selection(
        [('classic', 'Clásico'), ('certification', 'Reconocimiento'),
         ('homologar', 'Certificación')],
        string="Tipo de pantalla", default='classic')
    ch = fields.Boolean(string='Certificación', related='line_type_id.ch',
                        store=True)
    tipo_certificacion = fields.Many2one(
        'sicpro.app.trabajadores.educacion.certificacion',
        string="Tipo de Certificación")
    dias_validacion = fields.Integer(string='Días', required=False,
                                     related='tipo_certificacion.dias',
                                     store=True)
    fecha_expiracion = fields.Date(string='Fecha de Expiración',)
    active = fields.Boolean('Activo', default=True)
    correo_seguidores = fields.Char(string="correo_seguidores", index=True)

    date_start_formated = fields.Char(compute='_date_start_formated')
    date_end_formated = fields.Char(compute='_date_end_formated')
    fecha_expiracion_formated = fields.Char(compute='_fecha_expiracion_formated')

    def _date_start_formated(self):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        for part in self:
            part.date_start_formated = datetime.strftime(
                pytz.utc.localize(part.date_start).astimezone(local),
                "%d/%m/%Y, %H:%M:%S")

    def _date_end_formated(self):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        for part in self:
            part.date_end_formated = datetime.strftime(
                pytz.utc.localize(part.date_end).astimezone(local),
                "%d/%m/%Y, %H:%M:%S")

    def _fecha_expiracion_formated(self):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        for part in self:
            part.fecha_expiracion_formated = datetime.strftime(
                pytz.utc.localize(part.fecha_expiracion).astimezone(local),
                "%d/%m/%Y, %H:%M:%S")

    _sql_constraints = [(
        'date_check', "CHECK ((date_start <= date_end OR date_end = NULL))",
        "La fecha de inicio debe ser anterior a la fecha de finalización.."), ]

    @api.onchange('display_type')
    def onchange_display_type(self):
        if self.display_type == 'homologar' and not self.ch:
            self.display_type = None
            raise ValidationError(
                _('Esta pantalla solo esta disponible para el tipo de '
                  'educación: "Certificación y Homologación Personas" !!'))
        elif self.display_type in ('classic', 'certification') and self.ch:
            self.display_type = None
            raise ValidationError(
                _('El tipo de educación: "Certificación y Homologación '
                  'Personas" solo acepta la pantalla de Certificación !!'))

    @api.depends('tipo_certificacion', 'date_end')
    @api.onchange('date_end')
    def _onchange_fecha_expiracion(self):
        if self.tipo_certificacion and self.date_end:
            date_1 = fields.Date.from_string(self.date_end)
            date_2 = date_1 + relativedelta(days=self.dias_validacion)
            self.fecha_expiracion = date_2
        else:
            self.fecha_expiracion = None

    @api.onchange('line_type_id')
    def onchange_line_type_id(self):
        if self.ch:
            self.name = None
            self.display_type = 'homologar'
        else:
            self.display_type = 'classic'
            self.tipo_certificacion = False

    @api.onchange('tipo_certificacion')
    def onchange_tipo_certificacion(self):
        if self.tipo_certificacion:
            self.name = self.tipo_certificacion.name
        else:
            self.name = None

    # desactivo la certificación del trabajador y envío notificación y correo
    def send_expira_certificacion_mail(self):
        date = str(datetime.now().date().strftime('%d/%m/%Y'))
        trabajador = self.env[
            'sicpro.app.trabajadores.educacion'].search(
            ['&', ('active', '=', True), ('fecha_expiracion', '=', date)])
        if trabajador:
            for emp in trabajador:
                # busco el lider del grupo de atención al trabajador
                lider = emp.employee_id.equipo_tecnico.lider.user_id
                # busco los técnicos que atienden al trabajador
                tecnicos = emp.employee_id.tecnicos.user_id
                # busco los responsables de la aplicación de trabajadores
                responsables = self.env.ref(
                    'sicpro_app_trabajadores.grupo_app_trabajador_responsable').users
                # busco los encargado de capacitación
                capacitador = self.env.ref(
                    'sicpro_app_trabajadores.grupo_app_trabajador_capacitacion').users
                # creo la lista de seguidores
                seguidores = tecnicos + lider + responsables + capacitador
                # agrego los seguidores al modelo
                emp.message_subscribe(partner_ids=seguidores.partner_id.ids)
                # envió la notificación a los seguidores
                emp.message_post(body='Expiró una Certificación u Homologación',
                                 message_type='notification',
                                 subtype_xmlid='mail.mt_comment',
                                 author_id=self.env.user.partner_id.id)
                # desactivo el registro
                emp.active = False
                # mantiene actualizado el correo de los seguidores del registro
                correos = ''
                for follower in emp.message_partner_ids:
                    correos = str(correos) + str(follower.email_formatted)
                emp.correo_seguidores = correos
                # envío el correo a los implicados
                template = self.env.ref(
                    'sicpro_app_trabajadores.trabajadores_certificaciones_expira')
                template.send_mail(emp.id, force_send=True)
