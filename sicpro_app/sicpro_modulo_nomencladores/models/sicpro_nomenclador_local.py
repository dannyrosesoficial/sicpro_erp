# -*- coding: utf-8 -*-

from odoo import models, fields


class NomencladorLocales(models.Model):
    _name = 'sicpro.nomenclador.locales'
    _description = 'Locales de Centros de Costos'
    _order = "id"

    name = fields.Char(required=True, string='Local')
    centro_costo_usd = fields.Many2one(
        string='Centro Costo USD', required=True,
        comodel_name='sicpro.nomenclador.centro.costo', )
    centro_costo_cup = fields.Char('Centro Costo CUP',
                                   required=True,
                                   related='centro_costo_usd.centro_costo_cup')
    company_id = fields.Many2one(comodel_name="res.company", string="Proceso",
                                 related='centro_costo_usd.company_id',
                                 required=True, )
    active = fields.Boolean(string="Activo", default=True, )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El local ya existe !"),
    ]
