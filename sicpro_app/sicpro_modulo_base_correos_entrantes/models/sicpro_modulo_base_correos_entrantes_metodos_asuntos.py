# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class CorreosEntrantesAsuntos(models.Model):
    _name = 'sicpro.modulo.base.correos.entrantes.asuntos'
    _description = 'Asuntos para ejecutar los métodos en la entrada de un correo'
    _order = "id asc"

    name = fields.Char('Asunto', required=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    _sql_constraints = [('name_uniq', 'unique (name)', "¡El asunto ya existe!"), ]
