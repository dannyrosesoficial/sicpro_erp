# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class TrabajadoresFamiliar(models.Model):
    _name = "sicpro.app.trabajadores.familiar"
    _description = "Relaciones de los familiares del trabajador"

    name = fields.Char(string="Relación", required=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la relación existe!"),
    ]
