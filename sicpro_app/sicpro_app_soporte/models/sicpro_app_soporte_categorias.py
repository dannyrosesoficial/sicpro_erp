# -*- coding: utf-8 -*-

from odoo import fields, models


class SoporteCategoria(models.Model):

    _name = 'sicpro.app.soporte.categoria'
    _description = 'Categoría para el ticket del soporte'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Nombre', required=True)
    company_id = fields.Many2one('res.company', string="Company",
        default=lambda self: self.env['res.company']._company_default_get(
            'sicpro.app.soporte')
    )
