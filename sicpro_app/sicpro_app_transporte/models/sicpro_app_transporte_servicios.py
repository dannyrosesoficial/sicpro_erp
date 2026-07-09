# -*- coding: utf-8 -*-

from odoo import api, fields, models


class TransporteServicios(models.Model):
    _name = 'sicpro.app.transporte.servicios'
    _inherits = {'sicpro.app.transporte.costo': 'cost_id'}
    _description = 'Servicios del vehículo'

    @api.model
    def default_get(self, default_fields):
        res = super(TransporteServicios, self).default_get(default_fields)
        service = self.env.ref('sicpro_app_transporte.type_service_service_8',
                               raise_if_not_found=False)
        res.update({
            'date': fields.Date.context_today(self),
            'cost_subtype_id': service and service.id or False,
            'cost_type': 'servicios'
        })
        return res

    chofer = fields.Many2one('sicpro.app.trabajadores.general', 'Chofer')
    inv_ref = fields.Char('Referencia factura')
    responsable = fields.Many2one('res.users', 'Responsable',
                                  default=lambda self: self.env.user)
    # we need to keep this field as a related with store=True because
    # the graph view doesn't support
    # (1) to address fields from inherited table and (2) fields
    # that aren't stored in database
    cost_amount = fields.Float(related='cost_id.amount', string='Amount',
                               store=True, readonly=False)
    notes = fields.Text()
    cost_id = fields.Many2one('sicpro.app.transporte.costo', 'Costos',
                              required=True, ondelete='cascade')

    @api.onchange('vehicle_id')
    def _onchange_vehicle(self):
        if self.vehicle_id:
            self.odometer_unit = self.vehicle_id.odometer_unit
            self.chofer = self.vehicle_id.driver_id
