# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api, _


def _default_color():
    return randint(1, 11)


class ProductosEtiquetas(models.Model):
    _name = "sicpro.app.materiales.insumos.etiquetas"
    _description = "Etiquetas de los productos"

    name = fields.Char('Nombre de la etiqueta', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]