# -*- coding: utf-8 -*-


from random import randint
from odoo import fields, models, api


def _default_color():
    return randint(1, 11)


class AppCMIAccionesModoControl(models.Model):
    _name = 'sicpro.app.cmi.acciones.modo.control'
    _order = "id asc"
    _description = 'Modo de Control de las acciones'

    name = fields.Char('Nombre', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de control existe!"),
    ]
