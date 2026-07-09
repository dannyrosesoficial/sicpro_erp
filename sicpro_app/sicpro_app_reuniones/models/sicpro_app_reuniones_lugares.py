# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api, _


class ReunionesLugares(models.Model):
    _name = 'sicpro.app.reuniones.lugares'
    _description = 'Lugares de las Reuniones'

    # Crear la secuencia de incremento en el campo color.
    def _default_color(self):
        return randint(1, 11)

    name = fields.Char('Lugar', required=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=False)
    descripcion = fields.Char(string='Descripción',)
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre del lugar existe!"),
    ]