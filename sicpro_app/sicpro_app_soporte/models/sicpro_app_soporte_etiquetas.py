# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class SoporteEtiquetas(models.Model):
    _name = 'sicpro.app.soporte.etiquetas'
    _description = 'Etiquetas del Soporte'
    _order = "sequence, id"

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Nombre', required=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    sequence = fields.Integer('Secuencia', default=1, )
    solicitudes_acceso = fields.Boolean(string='Etiquetas/Acceso', default=False, required=False)
