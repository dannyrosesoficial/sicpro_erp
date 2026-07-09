# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductosUM(models.Model):
    _name = "sicpro.app.materiales.insumos.um"
    _description = "UM de los productos"

    name = fields.Char('UM', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "La etiqueta ya existe !"),
    ]
