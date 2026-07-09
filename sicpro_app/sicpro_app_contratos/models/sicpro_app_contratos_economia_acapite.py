# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ContratosEconomiaAcapite(models.Model):
    _name = 'sicpro.app.contratos.economia.acapite'
    _description = 'Acápites económicos de los contratos'
    _order = "id"

    name = fields.Char('Acápites', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre del Acápite existe!"),
    ]
