# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class MetrologiaCentroCalibracion(models.Model):
    _name = 'sicpro.app.metrologia.centro.calibracion'
    _description = 'Centro de Calibración Metrología'

    name = fields.Char(string="Nombre", required=True, )
    active = fields.Boolean(string="Activo", default=True, )
    color = fields.Integer(string='Color', default=lambda self: _default_color())
