# -*- coding: utf-8 -*-


from random import randint
from odoo import fields, models, api


def _default_color():
    return randint(1, 11)


class AppCMIAccionesEstado(models.Model):
    _name = 'sicpro.app.cmi.acciones.estado'
    _order = "id asc"
    _description = 'Estado de las acciones'

    name = fields.Char('Nombre', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    inicial = fields.Boolean(string='Inicial', required=False)
    final = fields.Boolean(string='Final', required=False)
    cancelado = fields.Boolean(string='Cancelado', required=False)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El estado existe!"),
    ]
