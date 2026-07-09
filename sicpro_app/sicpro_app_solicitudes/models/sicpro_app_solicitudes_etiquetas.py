# -*- coding: utf-8 -*-

from odoo import fields, models, api
from random import randint


class SolicitudesEtiquetas(models.Model):
    _name = "sicpro.app.solicitudes.etiquetas"
    _description = "Etiquetas de las Solicitudes"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char('Nombre de la etiqueta', required=True, translate=True)
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]
