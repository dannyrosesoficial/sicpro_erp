# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from random import randint


class SalonClasesEtiquetas(models.Model):
    _name = "sicpro.app.salon.clases.etiquetas"
    _description = "Etiquetas del Salón de clases"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char('Etiqueta', required=True)
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"), ]
