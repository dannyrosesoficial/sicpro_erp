# -*- coding: utf-8 -*-


from random import randint

from odoo import fields, models, api, _
from odoo.exceptions import UserError


def _default_color():
    return randint(1, 11)


class AppCMIAcciones(models.Model):
    _name = 'sicpro.app.cmi.acciones'
    _order = "id asc"
    _description = 'Acciones del CMI'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _estado_inicial(self):
        estado_id = self.env['sicpro.app.cmi.acciones.estado'].search(
            [('inicial', '=', True)]).id
        return estado_id

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo \
            as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.\
                NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char('Acción', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              tracking=True, default=lambda self: self.env.uid)
    responsable_id = fields.Many2one('res.users', string='Responsable',
                                     index=True, required=True)
    controla_id = fields.Many2one('res.users', string='Controla', index=True,
                                  required=True)
    participantes_ids = fields.Many2many('res.users', string="Participantes")
    estado_id = fields.Many2one('sicpro.app.cmi.acciones.estado', index=True,
                                string='Estado', default=_estado_inicial)
    estado_terminado = fields.Boolean(string='Estado Terminado', store=True,
                                      related="estado_id.final",
                                      required=False)
    modo_control = fields.Many2one('sicpro.app.cmi.acciones.modo.control',
                                   string='Modo de control', index=True, )
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, tracking=True, )
    seguir = fields.Boolean(string="Seguimiento", default=False, tracking=True)
    indicador_id = fields.Many2one('sicpro.app.cmi.indicadores', 'Indicadores',
                                   required=False, index=True)
    anio = fields.Char(string="Año", required=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    fecha_inicio = fields.Date(string="Fecha inicial", required=True,
                               default=lambda self: fields.Datetime.now())
    fecha_fin = fields.Date(string="Fecha Cumplimiento", required=True)
    control_fecha_inicio = fields.Boolean(string='Control_fecha_inicio',
                                          default=False)
    control_fecha_fin = fields.Boolean(string='Control_fecha_fin',
                                       default=False)
    grupo_responsable = fields.Boolean(string='grupo_responsable',
                                       compute="_compute_grupo_responsable")

    # verifica q el usuario activo pertenezca al grupo Responsable
    def _compute_grupo_responsable(self):
        self.grupo_responsable = self.env['res.users'].has_group(
            'sicpro_app_cmi.grupo_app_cmi_responsable')

    # envía correo al cambiar los estados
    @api.onchange('estado_id')
    def _onchange_estado(self):
        if not self.estado_id.inicial:
            # actualizo el valor del estado de forma recurrente para que lo
            # registre la plantilla de correo
            self.env['sicpro.app.cmi.acciones'].search(
                [('id', '=', self._origin.id)]).update(
                {'estado_id': self.estado_id})

            if self.seguir:
                # actualizo los usuario que recibirán el correo
                responsables_cmi = self.env.ref(
                    'sicpro_app_cmi.grupo_app_cmi_responsable').users
                responsable_accion = self.responsable_id
                controla_accion = self.controla_id
                correos = ''
                for item in responsables_cmi:
                    correos = str(correos) + str(item.partner_id.email_formatted)
                correos = str(correos) + str(
                    responsable_accion.partner_id.email_formatted) + str(
                    controla_accion.partner_id.email_formatted)
                email_values = {'email_to': correos, }

                # envío el correo a los seguidores del registro
                local_context = self.env.context.copy()
                template = self.env.ref(
                    'sicpro_app_cmi.cmi_cambio_estados_acciones')
                template.with_context(local_context).send_mail(
                    self._origin.id, force_send=True,
                    email_values=email_values)

    # verifica que la fecha de terminación no sea anterior a la de inicio
    @api.depends('fecha_inicio')
    @api.onchange('fecha_fin')
    def _onchange_fecha_fin(self):
        if self.fecha_fin:
            if self.fecha_fin < self.fecha_inicio:
                self.fecha_fin = None
                raise UserError(
                    _('La fecha de terminación de la acción no puede ser menor'
                      ' que la fecha de inicio, verifíquelo.'))

    # método de verificación de la fecha de inicio y terminación del cron
    @api.model
    def acciones_vencimiento_acciones(self):
        # ejecución del control de la fecha inicial
        inicial = self.env['sicpro.app.cmi.acciones'].search(
            [('estado_id.final', '=', False),
             ('estado_id.cancelado', '=', False),
             ('control_fecha_inicio', '=', False)])
        for item in inicial:
            if item.fecha_fin >= fields.Date.context_today(self):
                # mantiene actualizado el correo de seguidores del registro
                responsables_cmi = self.env.ref(
                    'sicpro_app_cmi.grupo_app_cmi_responsable').users
                responsable_accion = item.responsable_id
                controla_accion = item.controla_id
                correos = ''
                for data in responsables_cmi:
                    correos = str(correos) + str(
                        data.partner_id.email_formatted)
                correos = str(correos) + str(
                    responsable_accion.partner_id.email_formatted) + str(
                    controla_accion.partner_id.email_formatted)
                email_values = {'email_to': correos, }
                # envío el correo a los seguidores del registro
                local_context = item.env.context.copy()
                template = item.env.ref(
                    'sicpro_app_cmi.cmi_inicio_acciones')
                template.with_context(local_context).send_mail(item.id,
                    force_send=True, email_values=email_values)
                # actualizo el control de fecha inicial
                self.env['sicpro.app.cmi.acciones'].search(
                    [('id', '=', item.id)]).update({'control_fecha_inicio': True})

        # ejecución del control de las fecha fin
        fin = self.env['sicpro.app.cmi.acciones'].search(
            ['&', ('estado_id.final', '=', False),
             ('estado_id.cancelado', '=', False),
                ('control_fecha_fin', '=', False)])
        for item in fin:
            if item.fecha_fin <= fields.Date.context_today(self):
                # mantiene actualizado el correo de seguidores del registro
                responsables_cmi = self.env.ref(
                    'sicpro_app_cmi.grupo_app_cmi_responsable').users
                responsable_accion = item.responsable_id
                controla_accion = item.controla_id
                correos = ''
                for data in responsables_cmi:
                    correos = str(correos) + str(
                        data.partner_id.email_formatted)
                correos = str(correos) + str(
                    responsable_accion.partner_id.email_formatted) + str(
                    controla_accion.partner_id.email_formatted)
                email_values = {'email_to': correos, }
                # envío el correo a los seguidores del registro
                local_context = item.env.context.copy()
                template = item.env.ref(
                    'sicpro_app_cmi.cmi_vencimiento_acciones')
                template.with_context(local_context).send_mail(item.id,
                    force_send=True, email_values=email_values)
                # actualizo el control de fecha terminada
                self.env['sicpro.app.cmi.acciones'].search(
                    [('id', '=', item.id)]).update({'control_fecha_fin': True})
