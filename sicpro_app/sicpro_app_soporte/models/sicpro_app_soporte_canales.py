# -*- coding: utf-8 -*-

from random import randint

from odoo import models, fields


def _default_color():
    return randint(1, 11)


class SoporteCanales(models.Model):
    _name = 'sicpro.app.soporte.canales'
    _description = 'Canales de Solicitud'
    _order = "sequence, id"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string="Proceso", default=lambda self: self.env.company)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    code = fields.Char(string='Código', required=False)
    sequence = fields.Integer('Secuencia', default=1, )
