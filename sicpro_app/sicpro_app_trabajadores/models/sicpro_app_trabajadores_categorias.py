# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api


class TrabajadoresCategorias(models.Model):
    _name = "sicpro.app.trabajadores.categorias"
    _description = "Etiquetas de los trabajadores"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Nombre de la etiqueta", required=True)
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())
    tipo = fields.Selection(string='Tipo',
                            selection=[('contrato', 'Clase de Contrato'),
                                       ('ocupacional', 'Categoría Ocupacional'), ],
                            required=True,)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]
