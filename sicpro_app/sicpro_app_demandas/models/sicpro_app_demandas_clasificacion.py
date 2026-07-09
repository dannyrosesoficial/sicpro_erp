# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api, _


class DemandasClasificacion(models.Model):
    _name = 'sicpro.app.demandas.clasificacion'
    _description = 'Clasificación de la Demandas'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char('Clasificación', required=True)
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)',
         "La clasificación de demanda ya existe!"),
    ]
