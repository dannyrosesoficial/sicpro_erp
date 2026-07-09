# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class TrabajadoresCategorias(models.Model):
    _name = "sicpro.app.trabajadores.categorias"
    _description = "Etiquetas de los trabajadores"

    name = fields.Char(string="Nombre de la etiqueta", required=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    tipo = fields.Selection(string='Tipo', required=True,
                            selection=[('contrato', 'Clase de Contrato'), ('ocupacional', 'Categoría Ocupacional'), ], )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]
