# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from odoo import fields, api, models, _

_logger = logging.getLogger(__name__)


class IrCron(models.Model):
    _inherit = 'ir.cron'

    enable_history = fields.Boolean(string='Guardar Historial')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)

    @api.model
    def _callback(self, cron_name, server_action_id, job_id):
        cron = self.env['ir.cron'].sudo().browse(job_id)
        cron_history = False
        if cron.enable_history:
            cron_history = self.env['ir.cron.history']._create_history(
                cron_name, server_action_id)
            self = self.with_context(cron_history_id=cron_history.id)
        super(IrCron, self)._callback(cron_name, server_action_id, job_id)
        if cron_history:
            cron_history._done_history()

    @api.model
    def _trigger_alert(self, job_id, job_exception):
        # busco los usuarios con permisos a recibir los correos de alerta
        admin = self.env['res.users'].sudo().search(
            [('groups_id', 'in', self.env.ref('sicpro_app_administracion.grupo_app_administracion_notificaciones').id)])
        notifica = ''
        for value in admin:
            notifica = str(notifica) + str(value.partner_id.email_formatted)
        email_values = {'email_to': notifica, }

        if admin:
            template = self.env.ref('sicpro_modulo_historial_cron.plantilla_cron_fallido', raise_if_not_found=True)
            return template.with_context(date=datetime.now(), exception=job_exception.name
                if hasattr(job_exception, 'name') else job_exception
            ).send_mail(job_id, force_send=True, email_values=email_values)
        else:
            _logger.warning(
                _('No se puede enviar el correo, él servidor mail no esta configurado'))

    @api.model
    def _handle_callback_exception(
            self, cron_name, server_action_id, job_id, job_exception):
        super(IrCron, self)._handle_callback_exception(cron_name, server_action_id, job_id, job_exception)
        self.env['ir.cron.history']._error_history(job_exception)
        self._trigger_alert(job_id, job_exception)
