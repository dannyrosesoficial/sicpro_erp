# -*- coding: utf-8 -*-

from odoo import fields, models


class TransporteTipoCombustible(models.Model):
    _name = 'sicpro.app.transporte.tipo.combustible'
    _description = 'Tipo de Combustible para el Transporte'
    _order = 'name asc'

    name = fields.Char('Nombre', required=True)
    categoria = fields.Selection(
        string='Categoría', required=True, default='diesel',
        selection=[('diesel', 'Diesel'), ('especial', 'Especial'),
                   ('regular', 'Regular')])
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Currency', readonly=True,
                                       related='company_id.currency_id')
    costo = fields.Monetary(string='Costo', required=True,
                            currency_field='company_currency')

    _sql_constraints = [(
        'name_uniq', 'unique (name)', "El tipo de combustible ya existe!"), ]
