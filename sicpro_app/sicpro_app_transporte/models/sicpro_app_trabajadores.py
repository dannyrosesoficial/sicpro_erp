from odoo import api, models, fields


class TransporteTrabajadores(models.Model):
    _inherit = 'sicpro.app.trabajadores'

    transporte_id = fields.Many2one('sicpro.app.transporte.general', string='Chofer')

    transporte_count = fields.Integer('Vehículo',
                                      compute='_compute_vehiculos_count')

    @api.depends('transporte_id')
    def _compute_vehiculos_count(self):
        for trabajadores in self:
            trabajadores.transporte_count = len(trabajadores.transporte_id)
