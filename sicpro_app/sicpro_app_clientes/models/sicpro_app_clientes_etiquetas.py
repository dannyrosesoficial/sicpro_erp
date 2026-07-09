# -*- coding: utf-8 -*-


from random import randint
from odoo import fields, models, api


def _default_color():
    return randint(1, 11)


class AppClientesEtiquetas(models.Model):
    _name = 'sicpro.app.clientes.etiquetas'
    _order = "id asc"
    _description = 'Etiquetas para la Aplicación de Clientes'

    name = fields.Char('Etiqueta', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]
