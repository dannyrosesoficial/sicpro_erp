# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class DesactivarUsuarioDias(models.Model):
    _name = 'sicpro.app.modulo.usuario.desactivar.dias'
    _description = 'Aviso en días para la desactivación de los usuarios'
    _order = "id asc"

    name = fields.Integer('Días', required=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    _sql_constraints = [('name_uniq', 'unique (name)', "¡El día ya existe!"), ]
