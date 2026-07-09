# -*- coding: utf-8 -*-


from odoo import api, fields, models


class TransporteOdometro(models.Model):
    _name = 'sicpro.app.transporte.odometro'
    _description = 'Odometros del transporte'
    _order = 'date desc'

    name = fields.Char(string="Nombre", compute='_compute_vehicle_log_name',
                       store=True)
    date = fields.Date(string="Fecha", default=fields.Date.context_today)
    value = fields.Float('Valor de odómetro', group_operator="max")
    vehicle_id = fields.Many2one('sicpro.app.transporte.general', 'Vehículo',
                                 required=True)
    unit = fields.Selection(related='vehicle_id.odometer_unit',
                            string="Unidad", readonly=True)
    driver_id = fields.Many2one(related="vehicle_id.driver_id",
                                string="Trabajador", readonly=False)

    @api.depends('vehicle_id', 'date')
    def _compute_vehicle_log_name(self):
        for record in self:
            name = record.vehicle_id.name
            if not name:
                name = str(record.date)
            elif record.date:
                name += ' / ' + str(record.date)
            record.name = name

    @api.onchange('vehicle_id')
    def _onchange_vehicle(self):
        if self.vehicle_id:
            self.unit = self.vehicle_id.odometer_unit
