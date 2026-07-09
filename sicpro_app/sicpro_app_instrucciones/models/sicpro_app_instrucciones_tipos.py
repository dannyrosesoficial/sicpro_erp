# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api, _


class InstruccionesTipos(models.Model):
    _name = 'sicpro.app.instrucciones.tipos'
    _description = 'Tipos de Instrucciones'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char('Tipo', required=True)
    abreviatura = fields.Char('Abreviatura', required=True)
    color = fields.Integer(string='Color Index',
        default=lambda self: self._default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)',
         "El nombre del tipo de Instrucción existe!"),
    ]
