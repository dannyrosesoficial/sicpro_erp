# -*- coding: utf-8 -*-

from odoo import models, fields


class ColorsConfig(models.Model):
    _name = 'sicpro.modulo.dashboard.colores'
    _description = 'Colores - Nomenclador de Colores'

    name = fields.Char(required=True, string='Nombre')
    color = fields.Char(required=True, string='Color')
    active = fields.Boolean(string="Activo", default=True)


class ColorsOrderConfig(models.Model):
    _name = 'sicpro.modulo.dashboard.colores.orden'
    _description = 'Colores - Color con orden'
    _order = 'orden asc,id asc'

    orden = fields.Integer(
        string='Orden',
        required=True,
        help='Orden en que se usarán los colores'
    )
    color_set = fields.Many2one(
        'sicpro.modulo.dashboard.colores.set',
        string='Set al que pertenece',
        ondelete='cascade',
    )
    color = fields.Char(required=True, string='Color', default="#FFFFFF")
    active = fields.Boolean(string="Activo", default=True)


class ColorsDataSetConfig(models.Model):
    _name = 'sicpro.modulo.dashboard.colores.set'
    _description = 'Colores - Set de colores'

    name = fields.Char(required=True, string='Nombre')
    colores = fields.One2many(
        'sicpro.modulo.dashboard.colores.orden',
        string='Colores',
        inverse_name='color_set',
    )
    active = fields.Boolean(string="Activo", default=True)
