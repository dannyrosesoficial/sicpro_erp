# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api, _


def _default_color():
    return randint(1, 11)


class ContratosEconomiaPago(models.Model):
    _name = 'sicpro.app.contratos.economia.pago'
    _description = 'Forma de pago económico de los contratos'
    _order = "id"

    name = fields.Char('Forma de Pago', required=True)
    is_genera = fields.Boolean('¿Se Genera Consecutivo?')
    color = fields.Integer(string='Color',
        default=lambda self: _default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la forma de pago existe!"),
    ]
