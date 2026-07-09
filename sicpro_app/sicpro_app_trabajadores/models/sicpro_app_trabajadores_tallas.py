# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class TrabajadoresTallas(models.Model):
    _name = "sicpro.app.trabajadores.tallas"
    _description = "Tallas de los trabajadores"

    name = fields.Char(string="Nombre de la etiqueta", required=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "La talla ya existe!"),
    ]
