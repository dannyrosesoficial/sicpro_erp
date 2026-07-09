# -*- coding: utf-8 -*-

from odoo import api, fields, models


class TransporteCombustible(models.Model):
    _name = 'sicpro.app.transporte.combustible'
    _description = 'Registro de combustrible del transporte'
    _inherits = {'sicpro.app.transporte.costo': 'cost_id'}

    @api.model
    def default_get(self, default_fields):
        res = super(TransporteCombustible, self).default_get(default_fields)
        service = self.env['sicpro.app.transporte.tipo.servicios'].search(
            [('name', '=', "Reabastecimiento de combustible"), ])
        res.update({
            'date': fields.Date.context_today(self),
            'cost_subtype_id': service and service.id or False,
            'cost_type': 'combustible'
        })
        return res

    combustible = fields.Char(string="Combustible", required=True, )
    tarjeta_combustible = fields.Char(string="Tarjeta de Combustible",
                                      required=False, )
    vale_combustible = fields.Char(string="Vale de Combustible",
                                   required=False, )
    liter = fields.Float(string="Litros")
    price_per_liter = fields.Float(string="Precio por litro")
    quien_hecha_combustible = fields.Many2one(
        'sicpro.app.trabajadores.general', 'Habilita combustible')
    inv_ref = fields.Char('Referencia factura', size=64)
    notes = fields.Text(string="Notas")
    cost_id = fields.Many2one('sicpro.app.transporte.costo', 'Cost',
                              required=True, ondelete='cascade')
    # we need to keep this field as a related with store=True because
    # the graph view doesn't support
    # (1) to address fields from inherited table
    # (2) fields that aren't stored in database
    cost_amount = fields.Float(related='cost_id.amount', string='Amount',
                               store=True, readonly=False)

    @api.onchange('vehicle_id')
    def _onchange_vehicle(self):

        if self.vehicle_id:
            self.odometer_unit = self.vehicle_id.odometer_unit
            self.quien_hecha_combustible = self.vehicle_id.driver_id.id
            self.combustible = self.vehicle_id.combustible.name
            '''self.price_per_liter = self.combustible.precio'''
            self.price_per_liter = self.env['sicpro.app.transporte.tipo.combustible'].search(
                [('name', '=', self.combustible), ]).precio

    @api.onchange('liter', 'price_per_liter', 'amount')
    def _onchange_liter_price_amount(self):
        # need to cast in float because the value receveid from web client maybe an integer (Javascript and JSON do not
        # Modelo any difference between 3.0 and 3). This cause a problem if you encode, for example, 2 liters at 1.5 per
        # liter => total is computed as 3.0, then trigger an onchange that recomputes price_per_liter as 3/2=1 (instead
        # of 3.0/2=1.5)
        # If there is no change in the result, we return an empty dict to prevent an
        # infinite loop due to the 3 intertwine
        # onchange. And in order to verify that there is no change in the result, we have to limit the precision of the
        # computation to 2 decimal
        liter = float(self.liter)
        price_per_liter = float(self.price_per_liter)
        amount = float(self.amount)
        if liter > 0 and price_per_liter > 0 and round(liter * price_per_liter, 2) != amount:
            self.amount = round(liter * price_per_liter, 2)
        elif amount > 0 and liter > 0 and round(amount / liter, 2) != price_per_liter:
            self.price_per_liter = round(amount / liter, 2)
        elif amount > 0 and price_per_liter > 0 and round(amount / price_per_liter, 2) != liter:
            self.liter = round(amount / price_per_liter, 2)