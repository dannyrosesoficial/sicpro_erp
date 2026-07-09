# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class FuerzasMediosEtiquetas(models.Model):
    _name = "sicpro.app.fuerzas.medios.etiquetas"
    _description = "Etiquetas de las fuerzas y medios"

    name = fields.Char('Nombre de la etiqueta', required=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]
