from odoo import api, models, fields


class TransporteTrabajadores(models.Model):
    _inherit = 'sicpro.app.trabajadores.general'

    transporte_ids = fields.One2many(
        'sicpro.app.transporte.general', 'driver_id')
    transporte_count = fields.Integer('Vehículo',
                                      compute='_compute_vehiculos_count')

    @api.depends('transporte_ids')
    def _compute_vehiculos_count(self):
        for employee in self:
            employee.transporte_count = len(employee.transporte_ids)
