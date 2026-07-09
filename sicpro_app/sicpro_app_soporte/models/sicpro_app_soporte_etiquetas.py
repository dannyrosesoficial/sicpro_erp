# -*- coding: utf-8 -*-

from odoo import fields, models


class SoporteEtiquetas(models.Model):
    _name = 'sicpro.app.soporte.etiquetas'
    _description = 'Etiquetas del Soporte'

    name = fields.Char(string='Name')
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env['res.company']._company_default_get(
            'sicpro.app.soporte')
    )
