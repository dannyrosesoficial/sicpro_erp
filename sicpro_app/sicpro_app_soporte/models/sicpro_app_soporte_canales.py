# -*- coding: utf-8 -*-

from odoo import models, fields


class SoporteCanales(models.Model):

    _name = 'sicpro.app.soporte.canales'
    _description = 'Canales de Soporte'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env['res.company']._company_default_get(
            'sicpro.app.soporte')
    )
