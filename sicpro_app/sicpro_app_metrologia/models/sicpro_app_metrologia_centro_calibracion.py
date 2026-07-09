# -*- coding: utf-8 -*-

from odoo import fields, models


class MetrologiaCentroCalibracion(models.Model):
    _name = 'sicpro.app.metrologia.centro.calibracion'
    _description = 'Centro de Calibración'

    name = fields.Char(string="Nombre", required=True, )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)
    active = fields.Boolean(string="Activo", default=True, )
