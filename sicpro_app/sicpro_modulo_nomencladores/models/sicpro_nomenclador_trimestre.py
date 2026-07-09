# -*- coding: utf-8 -*-

from random import randint

from odoo import models, fields


def _default_color():
    return randint(1, 11)


class EstadosTrimestres(models.Model):
    _name = 'sicpro.nomenclador.trimestre'
    _description = 'Nomenclador de Trimestres'

    name = fields.Char(required=True, string='Trimestre')
    descripcion = fields.Char(string="Descripción", required=True, )
    active = fields.Boolean(string="Activo", default=True, )
    color = fields.Integer(string='Color', default=lambda self: _default_color())