# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class TransferenciasCuentasGastos(models.Model):
    _name = 'sicpro.app.transferencias.cuentas.gastos'
    _description = 'Cuentas de Gastos de las transferencias'

    name = fields.Char('Cuenta', required=True)
    descripcion = fields.Char('Descripción', required=True)
    active = fields.Boolean('Activo', default=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    traspasos = fields.Boolean(string='Traspasos', required=False, default=False,
                               help='Esta cuenta siempre es negativa. Es la que se utiliza para traspasarlos '
                                    'gastos a los territorios.')

    _sql_constraints = [('name_uniq', 'unique (name)', "La cuenta contable ya existe!"), ]

