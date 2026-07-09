# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class InstruccionesEtiquetas(models.Model):
    _name = 'sicpro.app.instrucciones.etiquetas'
    _description = 'Etiquetas de las Instrucciones'

    name = fields.Char('Etiqueta', required=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]
