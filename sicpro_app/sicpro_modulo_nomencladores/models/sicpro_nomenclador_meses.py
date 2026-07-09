# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint

from odoo import models, fields


def _default_color():
    return randint(1, 11)


class EstadosMeses(models.Model):
    _name = 'sicpro.nomenclador.meses'
    _description = 'Nomenclador de Meses'

    name = fields.Char(required=True, string='Mes')
    codigo_mes = fields.Integer(string="Código Mes", required=True)
    active = fields.Boolean(string="Activo", default=True, index=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
