# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class NomencladorSindicato(models.Model):
    _name = "sicpro.nomenclador.sindicato"
    _description = "Áreas sindicales de la DVPE"

    name = fields.Char('Sección Sindical', required=True)
    trabajador_id = fields.Many2one('sicpro.app.trabajadores', string='Responsable', required=True)
    user_id = fields.Many2one(comodel_name='res.users', string='Usuario', related='trabajador_id.user_id')
    areas_ids = fields.One2many('sicpro.app.trabajadores.areas', 'seccion_sindical_id', string='Áreas', required=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    _sql_constraints = [('name_uniq', 'unique (name)', "¡El nombre de la sección sindical ya existe!"), ]
