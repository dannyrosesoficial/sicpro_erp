# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ContratosEconomiaIndicador(models.Model):
    _name = 'sicpro.app.contratos.economia.indicador'
    _description = 'Indicadores económicos de los contratos'
    _order = "id"

    name = fields.Char('Indicadores', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre del indicador existe!"),
    ]
