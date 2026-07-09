# -*- coding: utf-8 -*-

from odoo import fields, models


class MetrologiaCentroCalibracion(models.Model):
    _name = 'sicpro.app.metrologia.centro.calibracion'
    _description = 'Centro de Calibración Metrología'

    name = fields.Char(string="Nombre", required=True, )
    active = fields.Boolean(string="Activo", default=True, )
