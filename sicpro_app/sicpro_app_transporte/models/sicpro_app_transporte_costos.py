# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TransporteCostos(models.Model):
    _name = 'sicpro.app.transporte.costo'
    _description = 'Costos relacionados al transporte'
    _order = 'date desc, vehicle_id asc'

    name = fields.Char(related='vehicle_id.name', string='Nombre',
                       store=True, readonly=False)
    vehicle_id = fields.Many2one('sicpro.app.transporte.general', 'Vehículo',
                                 required=True,
                                 help='Vehicle concerned by this log')
    cost_subtype_id = fields.Many2one('sicpro.app.transporte.tipo.servicios', 'Tipo',
                                      help='Cost type purchased with this cost')
    amount = fields.Float('Precio total')
    cost_type = fields.Selection([
        ('contratos', 'Contratos'),
        ('servicios', 'Servicios'),
        ('combustible', 'Combustible'),
        ('otros', 'Otros')
    ], 'Categorías de coste', default="otros",
        help='For internal purpose only', required=True)
    parent_id = fields.Many2one('sicpro.app.transporte.costo', 'Principal',
                                help='Parent cost to this current cost')
    cost_ids = fields.One2many('sicpro.app.transporte.costo', 'parent_id',
                               'Servicios incluidos', copy=True)
    odometer_id = fields.Many2one('sicpro.app.transporte.odometro', 'Odometer',
                                  help='Odometer measure of the vehicle at the moment of this log')
    odometer = fields.Float(compute="_get_odometer", inverse='_set_odometer',
                            string='Valor del odómetro',
                            help='Odometer measure of the vehicle at the moment of this log')
    odometer_unit = fields.Selection(related='vehicle_id.odometer_unit',
                                     string="Unidad", readonly=True)
    date = fields.Date(string="Fecha", help='Date when the cost has been executed')
    contract_id = fields.Many2one('sicpro.app.transporte.contratos', 'Contract',
                                  help='Contract attached to this cost')
    auto_generated = fields.Boolean('Generar automáticamente', readonly=True)
    description = fields.Char("Descripción del coste")
    company_id = fields.Many2one('res.company', 'Proceso',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    def _get_odometer(self):
        self.odometer = 0.0
        for record in self:
            record.odometer = False
            if record.odometer_id:
                record.odometer = record.odometer_id.value

    def _set_odometer(self):
        for record in self:
            if not record.odometer:
                raise UserError(_('Emptying the odometer value of a vehicle is not allowed.'))
            odometer = self.env['sicpro.app.transporte.odometro'].create({
                'value': record.odometer,
                'date': record.date or fields.Date.context_today(record),
                'vehicle_id': record.vehicle_id.id
            })
            self.odometer_id = odometer

    @api.model_create_multi
    def create(self, vals_list):
        for data in vals_list:
            # Modelo sure that the data are consistent with
            # values of parent and contract records given
            if 'parent_id' in data and data['parent_id']:
                parent = self.browse(data['parent_id'])
                data['vehicle_id'] = parent.vehicle_id.id
                data['date'] = parent.date
                data['cost_type'] = parent.cost_type
            if 'contract_id' in data and data['contract_id']:
                contract = self.env['sicpro.app.transporte.contratos'].browse(
                    data['contract_id'])
                data['vehicle_id'] = contract.vehicle_id.id
                data['cost_subtype_id'] = contract.cost_subtype_id.id
                data['cost_type'] = contract.cost_type
            if 'odometer' in data and not data['odometer']:
                # if received value for odometer is 0, then remove it from the
                # data as it would result to the creation of a
                # odometer log with 0, which is to be avoided
                del data['odometer']
        return super(TransporteCostos, self).create(vals_list)
