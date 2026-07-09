# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class ReunionesLugares(models.Model):
    _name = 'sicpro.app.reuniones.lugares'
    _description = 'Lugares de las Reuniones'

    # Crear la secuencia de incremento en el campo color.

    name = fields.Char('Lugar', required=True)
    company_id = fields.Many2one('res.company', string='Proceso', required=False)
    descripcion = fields.Char(string='Descripción', )
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    tipo = fields.Selection(string='Tipo', selection=[('interno', 'Interno'), ('externo', 'Externo'), ],
                            required=True, )

    _sql_constraints = [('name_uniq', 'unique (name)', "¡El nombre del lugar existe!"), ]
