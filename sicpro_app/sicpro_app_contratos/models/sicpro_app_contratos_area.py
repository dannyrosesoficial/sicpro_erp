# -*- coding: utf-8 -*-

from odoo import fields, models


class ContratosAreas(models.Model):
    _name = 'sicpro.app.contratos.areas'
    _description = 'Áreas de los contratos'
    _order = "id asc"

    name = fields.Char('Área', required=True)
    unidad = fields.Many2one('sicpro.app.contratos.unidades',
                             string='Unidad')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El área del contrato existe!"),
    ]
