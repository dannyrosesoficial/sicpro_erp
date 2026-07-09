# -*- coding: utf-8 -*-

from odoo import fields, models, api
from random import randint


class SoporteEtiquetas(models.Model):
    _name = 'sicpro.app.soporte.etiquetas'
    _description = 'Etiquetas del Soporte'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Name')
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company',  string="Company",
        default=lambda self: self.env['res.company']._company_default_get(
            'sicpro.app.soporte'))
