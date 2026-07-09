# -*- coding: utf-8 -*-

from random import randint

from odoo import models, fields


def _default_color():
    return randint(1, 11)


class ViviendaMateriales(models.Model):
    _name = 'sicpro.app.vivienda.materiales'
    _description = 'Materiales para el programa de la vivienda'

    name = fields.Char('Material', required=True)
    um = fields.Many2one(comodel_name='sicpro.app.vivienda.materiales.um', string='U/M', required=True)
    active = fields.Boolean('Activo', default=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    _sql_constraints = [('name_uniq', 'unique (name)', "¡El nombre del material ya existe!"), ]