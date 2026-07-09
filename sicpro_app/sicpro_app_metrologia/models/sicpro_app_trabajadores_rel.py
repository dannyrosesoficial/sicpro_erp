from odoo import api, models, fields


class Trabajadores(models.Model):
    _inherit = 'sicpro.app.trabajadores'

    equipment_ids = fields.One2many(
        'sicpro.app.metrologia.equipos', 'trabajador_id')
    equipment_count = fields.Integer('Equipos',
                                     compute='_compute_equipment_count')

    @api.depends('equipment_ids')
    def _compute_equipment_count(self):
        for employee in self:
            employee.equipment_count = len(employee.equipment_ids)
