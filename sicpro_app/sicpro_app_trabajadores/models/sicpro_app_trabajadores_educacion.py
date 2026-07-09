# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


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
    company_currency = fields.Many2one(string='Moneda', readonly=True,
                                       related='company_id.currency_id')
    pago = fields.Monetary(string='Pago', related='line_type_id.pago',
                           currency_field='company_currency', store=True)
    display_type = fields.Selection(
        [('classic', 'Clásico'), ('certification', 'Reconocimiento'),
         ('homologar', 'Certificación')], string="Tipo de pantalla",
        default='classic')
    ch = fields.Boolean(string='Certificación', related='line_type_id.ch',
                        store=True)
    tipo_certificacion = fields.Many2one(
        'sicpro.app.trabajadores.educacion.certificacion',
        string="Tipo de Certificación")
    dias_validacion = fields.Integer(string='Días', required=False,
                                     related='tipo_certificacion.dias',
                                     store=True)
    fecha_expiracion = fields.Date(string='Fecha de Expiración', )
    active = fields.Boolean(string='Activo', default=True)

    @api.constrains('date_start', 'date_end')
    def _check_dates_range(self):
        for record in self:
            # En Odoo/Python, NULL se evalúa como False
            if record.date_start and record.date_end:
                if record.date_start > record.date_end:
                    raise ValidationError(
                        "Inconsistencia de Fechas: La fecha de inicio (%s) "
                        "debe ser anterior o igual a la fecha de finalización (%s)." % (
                        record.date_start,
                        record.date_end) + MSG_SOPORTE_SICPRO)

    @api.onchange('display_type')
    def onchange_display_type(self):
        if self.display_type == 'homologar' and not self.ch:
            self.display_type = None
            raise ValidationError(
                'Esta pantalla solo esta disponible para el tipo de '
                '¡educación: "Certificación y Homologación Personas"!' + MSG_SOPORTE_SICPRO)
        elif self.display_type in ('classic', 'certification') and self.ch:
            self.display_type = None
            raise ValidationError(
                'El tipo de educación: "Certificación y Homologación Personas" '
                'solo acepta la pantalla de Certificación !!' + MSG_SOPORTE_SICPRO)

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
        expira = fields.Datetime.now()
        trabajador = self.env['sicpro.app.trabajadores.educacion'].search(
            ['&', ('active', '=', True), ('fecha_expiracion', '=', expira)])
        if trabajador:
            for emp in trabajador:
                # busco el líder del grupo de atención al trabajador
                lider = emp.employee_id.equipo_tecnico.lider.user_id
                # busco los técnicos que atienden al trabajador
                tecnicos = emp.employee_id.tecnicos.user_id
                # busco los responsables de la aplicación de trabajadores
                group_responsables = self.env.ref(
                    'sicpro_app_trabajadores.grupo_app_trabajador_responsable',
                    raise_if_not_found=False)
                responsables = self.env['res.users']
                if group_responsables:
                    responsables = group_responsables.user_ids
                # busco los encargado de capacitación
                group_capacitador = self.env.ref(
                    'sicpro_app_trabajadores.grupo_app_trabajador_capacitacion',
                    raise_if_not_found=False)
                capacitador = self.env['res.users']
                if group_capacitador:
                    capacitador = group_capacitador.user_ids
                # creo la lista de seguidores
                seguidores = tecnicos + lider + responsables + capacitador
                # agrego los seguidores al modelo
                emp.message_subscribe(partner_ids=seguidores.partner_id.ids)
                # envió la notificación a los seguidores
                emp.message_post(body='Certificación u Homologación expirada',
                                 message_type='notification',
                                 subtype_xmlid='mail.mt_comment',
                                 author_id=self.env.user.partner_id.id)
                # desactivo el registro
                emp.active = False

                for participante in emp.message_partner_ids:
                    # envío el correo electrónico
                    participantes = participante.email_formatted
                    email_values = {'email_to': participantes}
                    template = self.env.ref(
                        'sicpro_app_trabajadores.trabajadores_certificaciones_expira')
                    template.send_mail(emp.id, force_send=True,
                                       email_values=email_values, )
