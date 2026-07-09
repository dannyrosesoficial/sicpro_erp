# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api, _


class ContratosEconomiaPago(models.Model):
    _name = 'sicpro.app.contratos.economia.pago'
    _description = 'Forma de pago económico de los contratos'
    _order = "id"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char('Forma de Pago', required=True)
    is_genera = fields.Boolean('¿Se Genera Consecutivo?')
    color = fields.Integer(string='Color Index',
        default=lambda self: self._default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la forma de pago existe!"),
    ]
