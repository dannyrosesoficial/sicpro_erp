# -*- coding: utf-8 -*-

from odoo import fields, models, api
from random import randint


def _default_color():
    return randint(1, 11)


class SolicitudesEtiquetas(models.Model):
    _name = "sicpro.app.solicitudes.etiquetas"
    _description = "Etiquetas de las Solicitudes"

    name = fields.Char('Nombre de la etiqueta', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]
