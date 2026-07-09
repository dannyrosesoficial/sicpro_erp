# -*- coding: utf-8 -*-


from odoo import fields, models


class TransporteTipoServicio(models.Model):
    _name = 'sicpro.app.transporte.tipo.servicios'
    _description = 'Tipo de servicio del transporte'

    name = fields.Char(string="Nombre", required=True, translate=True)
    category = fields.Selection([
        ('contratos', 'Contratos'),
        ('servicios', 'Servicios')
    ], 'Category', required=True,
        help='Choose whether the service refer to '
             'contracts, vehicle services or both')
