# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class ViviendaEscalafon(models.Model):
    _name = "sicpro.app.vivienda.escalafon"
    _description = "Escalafón del programa de la vivienda"

    name = fields.Integer('Número', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "¡El número de escalafón ya existe!"),
    ]
