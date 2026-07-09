# -*- coding: utf-8 -*-

from odoo import fields, models


class ContratosProveedoresTipo(models.Model):
    _name = 'sicpro.app.contratos.proveedores.tipo'
    _description = 'Tipos de proveedores de los contratos'
    _order = "id asc"

    name = fields.Char('Tipos', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El tipo de proveedor existe!"),
    ]
