# -*- coding: utf-8 -*-


from random import randint
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


def _default_color():
    return randint(1, 11)


class AppCMIIndicadoresCambios(models.Model):
    _name = 'sicpro.app.cmi.indicadores.cambios'
    _order = "id asc"
    _description = 'Cambios de Indicadores del CMI'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    user_id = fields.Many2one('res.users', string='Usuario', index=True, default=lambda self: self.env.uid)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, )
    detalles = fields.Text(string="Detalles", required=False)
    observaciones = fields.Text(string="Observaciones", required=False)
    name = fields.Many2one('sicpro.app.cmi.indicadores', string='Indicador', required=False)
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    meta_actual = fields.Integer(string='Meta Actual', required=True)
    meta_propuesta = fields.Integer(string='Meta Propuesta', required=True)
    responsable_id = fields.Many2one('res.users', string='Responsable', index=True, required=True)
    attachment_ids = fields.Many2many('ir.attachment', string="Adjuntos")
    mes = fields.Selection(
        [('enero', 'Enero'), ('febrero', 'Febrero'), ('marzo', 'Marzo'), ('abril', 'Abril'), ('mayo', 'Mayo'),
         ('junio', 'Junio'), ('julio', 'Julio'), ('agosto', 'Agosto'), ('septiembre', 'Septiembre'),
         ('octubre', 'Octubre'), ('noviembre', 'Noviembre'), ('diciembre', 'Diciembre')], )
    estado = fields.Selection(
        [('pendiente', 'Pendiente'), ('revision', 'En Revisión'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')],
        default='pendiente')

    # ver historial de cambios de indicadores
    def cambios_historial_indicadores(self):
        active_id = self._context.get('default_id')
        active_mes = self._context.get('default_mes')
        action = self.env['ir.actions.act_window']._for_xml_id('sicpro_app_cmi.historial_cambios_indicadores_action')
        action['views'] = [(False, 'tree')]
        action['domain'] = ['&', ('name', '=', active_id), ('mes', '=', active_mes)]
        return action

    # pasar a revisión los cambios de indicadores
    def cambios_revision_indicadores(self):
        self.estado = 'revision'

    # aprobar cambios de indicadores
    def cambios_aprobar_indicadores(self):
        self.estado = 'aprobado'
        # actualizo el valor de la meta propuesta
        self.env['sicpro.app.cmi.indicadores.valores'].search(
            [('indicador_id', '=', self.name.id), ('mes', '=', self.mes)]).update({'meta': self.meta_propuesta})

        # llamo al método para crear la notificación
        post = self.env['sicpro.app.cmi.indicadores'].browse(self.name.id)
        self.message_subscribe(partner_ids=post.message_follower_ids.partner_id.ids)
        post.message_post(body='Cambio de Meta aprobado.', message_type='notification', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)

        # envío el correo a los seguidores del registro
        local_context = post.env.context.copy()
        template = post.env.ref('sicpro_app_cmi.cmi_cambio_indicador_aprobado')
        template.with_context(local_context).send_mail(post.id, force_send=True)

    # rechazar de cambios de indicadores
    def cambios_rechazar_indicadores(self):
        if self.observaciones:
            self.estado = 'rechazado'
            # llamo al método para crear la notificación
            post = self.env['sicpro.app.cmi.indicadores'].browse(self.name.id)
            self.message_subscribe(partner_ids=post.message_follower_ids.partner_id.ids)
            post.message_post(body='Cambio de Meta rechazado.', message_type='notification',
                              subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)
            # Selecciono el registro de seguidores
            for participante in self.message_partner_ids:
                # envío el correo electrónico
                email_values = {'email_to': participante.email_formatted, }
                local_context = post.env.context.copy()
                template = self.env.ref('sicpro_app_cmi.cmi_cambio_indicador_rechazado')
                template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        else:
            raise UserError(_('Debe argumentar el motivo del rechazo '
                              'en el campo de observaciones.'))
