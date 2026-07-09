# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SicproDBExplorerTable(models.Model):
    _name = 'sicpro.app.db.explorer.table'
    _description = 'Explorador de Tablas Maestro'
    _order = 'model asc'

    name = fields.Char(string="Nombre de la Tabla", related='model_id.name', store=True)
    model_id = fields.Many2one('ir.model', string="Modelo Odoo", required=True, ondelete='cascade')
    model = fields.Char(string="Técnico (Model)", related='model_id.model', store=True)
    count_records = fields.Integer(string="Registros", compute='_compute_count_records')
    is_protected = fields.Boolean(string="Protegida", default=False)
    state = fields.Selection([
        ('locked', 'Bloqueado'),
        ('unlocked', 'Modo Edición Activo')
    ], string="Estado de Seguridad", default='locked', readonly=True)

    audit_log_ids = fields.One2many('sicpro.app.db.audit.log', 'model_name',
                                    string="Logs de Auditoría",
                                    compute='_compute_audit_logs')

    def _compute_audit_logs(self):
        for record in self:
            record.audit_log_ids = self.env['sicpro.app.db.audit.log'].search([
                ('model_name', '=', record.model)
            ])

    def _compute_count_records(self):
        for record in self:
            try:
                record.count_records = self.env[record.model].search_count([])
            except:
                record.count_records = 0

    def action_open_table_data(self):
        """Abre la vista dinámica de la tabla seleccionada"""
        self.ensure_one()
        return {
            'name': _('Datos Crudos: %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': self.model,
            'view_mode': 'list,form',
            'target': 'current',
            'context': {'active_test': False}, # Para ver registros archivados
        }

    def action_unlock_request(self):
        """Llama al wizard de contraseña maestra"""
        return {
            'name': _('Verificación de Seguridad'),
            'type': 'ir.actions.act_window',
            'res_model': 'sicpro.app.db.master.password.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_table_id': self.id}
        }

    def action_view_audit_logs(self):
        """Abre la lista de auditoría filtrada por esta tabla"""
        self.ensure_one()
        return {
            'name': _('Auditoría: %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'sicpro.app.db.audit.log',
            'view_mode': 'list,form',
            'domain': [('model_name', '=', self.model)],
            'context': {'create': False},
        }
