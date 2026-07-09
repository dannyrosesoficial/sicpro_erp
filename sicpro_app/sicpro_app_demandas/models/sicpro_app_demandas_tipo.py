# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api, _


class DemandasTipos(models.Model):
    _name = 'sicpro.app.demandas.tipo'
    _description = 'Tipo de la Demandas'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char('Tipo', required=True)
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El tipo de demanda ya existe!"),
    ]
