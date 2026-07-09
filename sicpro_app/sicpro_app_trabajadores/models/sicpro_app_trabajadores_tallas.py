# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api


class TrabajadoresTallas(models.Model):
    _name = "sicpro.app.trabajadores.tallas"
    _description = "Tallas de los trabajadores"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Nombre de la etiqueta", required=True)
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "La talla ya existe!"),
    ]
