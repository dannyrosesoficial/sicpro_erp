# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import logging
from dateutil.relativedelta import relativedelta
from odoo import fields, api, models

_logger = logging.getLogger(__name__)


class IrCronHistory(models.Model):
    _name = 'ir.cron.history'
    _description = 'Historial de ejecución del Cron'
    _order = 'date_start desc'
    _inherits = {'ir.actions.server': 'ir_actions_server_id'}

    ir_actions_server_id = fields.Many2one('ir.actions.server',
                                           'Acción del Servidor',
                                           delegate=True, ondelete='cascade',
                                           required=True)
    action_name = fields.Char(string='Cron', readonly=True)
    date_start = fields.Datetime(string='Inicio',
                                 default=lambda self: fields.Datetime.now())
    date_end = fields.Datetime(string='Fin')
    state = fields.Selection(
        [('in_progress', 'En Progreso'), ('done', 'Ejecutado'),
         ('error', 'Error'), ('interrupted', 'Interrumpido'), ], 'Estado',
        default='in_progress', readonly=True)
    message_error = fields.Text(string='Mensaje de Error')

    @api.model
    def _create_history(self, cron_name, server_action_id):
        try:
            in_progress = self.search(
                [('ir_actions_server_id', '=', server_action_id),
                 ('state', '=', 'in_progress')])
            if in_progress:
                try:
                    in_progress.write({'state': 'interrupted'})
                except Exception:
                    # fallback con sudo si el usuario no tiene derechos
                    in_progress.sudo().write({'state': 'interrupted'})
        except Exception:
            _logger.exception(
                'Error marcando ejecuciones en progreso como interrumpidas')
        # Crear historial
        vals = {'ir_actions_server_id': server_action_id,
                'action_name': cron_name}
        try:
            cron_history = self.create(vals)
        except Exception:
            _logger.warning(
                'Creación de historial falló sin sudo, intentando con sudo()')
            cron_history = self.sudo().create(vals)
        return cron_history

    def _done_history(self):
        if not self:
            return False
        try:
            if self.state == 'in_progress':
                try:
                    self.write(
                        {'state': 'done', 'date_end': fields.Datetime.now()})
                except Exception:
                    self.sudo().write(
                        {'state': 'done', 'date_end': fields.Datetime.now()})
        except Exception:
            _logger.exception('Error marcando historial como done')

    @api.model
    def _error_history(self, job_exception):
        cron_history_id = self.env.context.get('cron_history_id')
        if cron_history_id:
            cron_history = self.env['ir.cron.history'].browse(
                cron_history_id).sudo()
            job_error = job_exception.name if hasattr(job_exception,
                                                      'name') else job_exception
            cron_history.write(
                {'state': 'error', 'date_end': fields.Datetime.now(),
                    'message_error': job_error, })

    @api.model
    def cron_cleanup_cron_history(self, days=90):
        _logger.info('Start cleanup cron history')
        try:
            cutoff = fields.Date.to_string(
                fields.Date.from_string(fields.Date.today()) - relativedelta(
                    days=days))
            cron_history = self.search([('create_date', '<', cutoff)])
            count = len(cron_history)
            _logger.info('Se limpiará el historial: %s registros', count)
            if cron_history:
                try:
                    cron_history.unlink()
                except Exception:
                    cron_history.sudo().unlink()
            _logger.info('Culmino la limpieza del historial de ejecución CRON')
        except Exception:
            _logger.exception('Error durante limpieza de historial cron')
