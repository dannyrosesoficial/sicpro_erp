# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging
from datetime import datetime
from odoo import fields, api, models

_logger = logging.getLogger(__name__)


class IrCron(models.Model):
    _inherit = 'ir.cron'

    enable_history = fields.Boolean(string='Guardar Historial')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)

    def _callback(self, cron_name, server_action_id):
        cron = self.sudo()
        cron_history = False
        try:
            if cron and cron.enable_history:
                try:
                    cron_history = self.env['ir.cron.history']._create_history(
                        cron_name, server_action_id)
                except Exception as create_err:
                    _logger.warning(
                        'No se pudo crear el historial sin sudo: %s. Intentando sudo().',
                        create_err)
                    cron_history = self.sudo().env[
                        'ir.cron.history']._create_history(cron_name,
                                                           server_action_id)
                # Pasamos el contexto para que la excepción pueda registrar en el historial
                self = self.with_context(cron_history_id=cron_history.id)
        except Exception:
            _logger.exception(
                'Error al preparar historial de cron (se continúa la ejecución).')

        super(IrCron, self)._callback(cron_name, server_action_id)

        # Marcar completado si se creó el historial
        if cron_history:
            try:
                cron_history._done_history()
            except Exception:
                _logger.exception('Error al marcar historial como done')

    @api.model
    def _trigger_alert(self, job_id, job_exception):
        group = None
        try:
            group = self.env.ref(
                'sicpro_app_administracion.grupo_app_administracion_notificaciones',
                raise_if_not_found=False)
        except Exception:
            group = None
        admins = self.env['res.users']
        if group:
            try:
                admins = self.env['res.users'].sudo().search(
                    [('groups_id', 'in', group.id)])
            except Exception:
                admins = self.env['res.users'].sudo().search(
                    [('groups_id', 'in', group.id)])
        emails = []
        for user in admins:
            if user.partner_id and user.partner_id.email:
                emails.append(user.partner_id.email)
        email_to = ','.join(emails)
        if emails:
            template = self.env.ref(
                'sicpro_modulo_historial_cron.plantilla_cron_fallido',
                raise_if_not_found=False)
            if template:
                try:
                    return template.with_context(
                        date=datetime.now(),
                        exception=(job_exception.name if hasattr(
                            job_exception, 'name') else
                                   job_exception)).send_mail(
                        job_id, force_send=True,
                        email_values={'email_to': email_to})
                except Exception:
                    _logger.exception(
                        'Error al enviar template de notificación de cron fallido')
            else:
                _logger.warning(
                    'Plantilla de notificación no encontrada: sicpro_modulo_historial_cron.plantilla_cron_fallido')
        else:
            _logger.warning(
                'No se encontraron administradores con correo para notificar.')

    @api.model
    def _handle_callback_exception(self, cron_name, server_action_id, job_id,
        job_exception):
        super(IrCron, self)._handle_callback_exception(cron_name,
                                                       server_action_id,
                                                       job_id, job_exception)
        self.env['ir.cron.history']._error_history(job_exception)
        self._trigger_alert(job_id, job_exception)
