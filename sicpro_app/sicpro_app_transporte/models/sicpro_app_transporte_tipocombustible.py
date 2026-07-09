# -*- coding: utf-8 -*-

from odoo import fields, models


class TransporteTipoCombustible(models.Model):
    _name = 'sicpro.app.transporte.tipo.combustible'
    _description = 'Combustible del vehículo'
    _order = 'name asc'

    name = fields.Char('Combustible', required=True)
    precio = fields.Float(string="Precio")
    active = fields.Boolean(string="Activo", default=True, )