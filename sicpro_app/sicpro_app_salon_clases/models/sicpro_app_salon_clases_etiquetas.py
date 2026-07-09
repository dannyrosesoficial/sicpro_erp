# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from random import randint


def _default_color():
    return randint(1, 11)


class SalonClasesEtiquetas(models.Model):
    _name = "sicpro.app.salon.clases.etiquetas"
    _description = "Etiquetas del Salón de clases"

    name = fields.Char('Etiqueta', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"), ]
