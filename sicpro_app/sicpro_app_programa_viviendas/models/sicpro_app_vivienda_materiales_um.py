# -*- coding: utf-8 -*-

from random import randint

from odoo import models, fields


def _default_color():
    return randint(1, 11)


class ViviendaMaterialesUM(models.Model):
    _name = 'sicpro.app.vivienda.materiales.um'
    _description = 'Unidad de medidas de los materiales'

    name = fields.Char('U/M', required=True)
    active = fields.Boolean('Activo', default=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    _sql_constraints = [('name_uniq', 'unique (name)', "¡La unidad de medida ya existe!"), ]
