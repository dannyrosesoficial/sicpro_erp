# -*- coding: utf-8 -*-

from odoo import fields, models


class ContratosTipo(models.Model):
    _name = 'sicpro.app.contratos.tipo'
    _description = 'Tipo de contratos'
    _order = "id asc"

    name = fields.Char('Tipo de contrato', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El tipo de contrato existe!"),
    ]
