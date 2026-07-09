# -*- coding: utf-8 -*-

from random import randint

from odoo import models, fields


def _default_color():
    return randint(1, 11)


class EstadosCuentasContables(models.Model):
    _name = 'sicpro.nomenclador.cuentas.contables'
    _description = 'Nomenclador Cuentas Contables'

    name = fields.Char(required=True, string='Cuentas')
    descripcion = fields.Char(string="Descripción", required=True, )
    active = fields.Boolean(string="Activo", default=True, )
    color = fields.Integer(string='Color', default=lambda self: _default_color())
