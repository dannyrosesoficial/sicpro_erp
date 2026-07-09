# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class ControlInformacionEtiquetas(models.Model):
    _name = "sicpro.app.control.informacion.etiquetas"
    _description = "Etiquetas del control de información"

    name = fields.Char('Nombre de la etiqueta', required=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    active = fields.Boolean('Activo', default=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]
