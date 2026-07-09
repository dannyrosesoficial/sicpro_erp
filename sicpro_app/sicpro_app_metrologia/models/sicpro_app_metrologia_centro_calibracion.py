# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint
from odoo import fields, models


def _default_color():
    return randint(1, 11)


class MetrologiaCentroCalibracion(models.Model):
    _name = 'sicpro.app.metrologia.centro.calibracion'
    _description = 'Centro de Calibración Metrología'

    name = fields.Char(string="Nombre", required=True, )
    active = fields.Boolean(string="Activo", default=True, index=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
