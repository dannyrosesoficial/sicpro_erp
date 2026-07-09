# -*- coding: utf-8 -*-

from random import randint

from odoo import models, fields


def _default_color():
    return randint(1, 11)


class EstadosMeses(models.Model):
    _name = 'sicpro.nomenclador.meses'
    _description = 'Nomenclador de Meses'

    name = fields.Char(required=True, string='Mes')
    codigo_mes = fields.Integer(string="Código Mes", required=True, )
    active = fields.Boolean(string="Activo", default=True, )
    color = fields.Integer(string='Color', default=lambda self: _default_color())
