# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class ViviendaProveedor(models.Model):
    _name = "sicpro.app.vivienda.proveedor"
    _description = "Proveedor del programa de la vivienda"

    name = fields.Char('Proveedor', required=True)
    active = fields.Boolean('Activo', default=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "¡El proveedor ya existe!"),
    ]
