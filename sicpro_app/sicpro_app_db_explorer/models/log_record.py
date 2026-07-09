# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models, fields, api
from datetime import timedelta


class LogRecord(models.Model):
    _name = 'sicpro.log.record'
    _description = 'Registro Histórico y Ciclo de Vida del Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'log_date desc'

    name = fields.Char(string="Referencia", required=True, copy=False,
                       readonly=True, default='Nuevo')
    source_id = fields.Many2one('sicpro.log.source', string="Fuente",
                                required=True, tracking=True)
    severity_id = fields.Many2one('sicpro.log.severity', string="Nivel",
                                  required=True, tracking=True)
    log_date = fields.Datetime(string="Fecha del Evento",
                               default=fields.Datetime.now, required=True)

    # Datos en crudo
    message = fields.Text(string="Mensaje del Log", required=True)
    trace_id = fields.Char(string="Trace ID (Correlación)")

    # Gestión del Ciclo de Vida (Histórico y Soluciones)
    state = fields.Selection(
        [('new', 'Nuevo Evento'), ('investigating', 'En Investigación'),
            ('resolved', 'Resuelto'), ('ignored', 'Ignorado')],
        string="Estado de Resolución", default='new', tracking=True)

    root_cause = fields.Text(string="Causa Raíz", tracking=True)
    solution_applied = fields.Text(string="Solución Aplicada", tracking=True)
    action_plan = fields.Text(string="Plan de Acción Futuro")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sicpro.log.record') or 'LOG-Nuevo'
        return super().create(vals_list)

    @api.model
    def _cron_cleanup_old_logs(self):
        # Limpieza de retención: Elimina logs INFO más antiguos de 7 días. Configurable en base de datos.
        date_limit = fields.Datetime.now() - timedelta(days=7)
        old_info_logs = self.search(
            [('severity_id.code', '=', 'info'), ('log_date', '<', date_limit),
                ('state', 'in', ['new', 'ignored', 'resolved'])])
        old_info_logs.unlink()
