# -*- coding: utf-8 -*-

from odoo import fields, models


class MetrologiaMagnitudes(models.Model):
    _name = 'sicpro.app.metrologia.magnitud'
    _description = 'Magnitudes'

    name = fields.Char(string="Magnitud", required=True, )
    magnitud_corta = fields.Char(string="Abreviatura", required=False, )
    active = fields.Boolean(sring="Activo", default=True, )
