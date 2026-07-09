# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from random import randint


def _default_color():
    return randint(1, 11)


class SalonClasesTipo(models.Model):
    _name = "sicpro.app.salon.clases.tipo"
    _description = "Tipo de temáticas"

    name = fields.Char('Nombre', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"), ]
