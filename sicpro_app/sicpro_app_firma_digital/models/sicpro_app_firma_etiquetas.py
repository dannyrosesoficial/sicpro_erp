# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api, _


def _default_color():
    return randint(1, 11)


class FirmaDigitalEtiquetas(models.Model):
    _name = 'sicpro.app.firma.etiquetas'
    _description = 'Etiquetas de la Firma Digital'

    name = fields.Char('Etiqueta', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]
