# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api, _


class ContratosProveedoresEtiquetas(models.Model):
    _name = 'sicpro.app.contratos.proveedores.etiquetas'
    _description = 'Etiquetas de proveedores de los contratos'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char('Etiqueta', required=True)
    color = fields.Integer(string='Color Index',
        default=lambda self: self._default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]
