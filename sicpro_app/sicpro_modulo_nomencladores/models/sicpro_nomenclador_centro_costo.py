# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NomencladorCentroCosto(models.Model):
    _name = 'sicpro.nomenclador.centro.costo'
    _description = 'Centros de Costos'

    name = fields.Char('Centro Costo USD', required=True)
    centro_costo_cup = fields.Char('Centro Costo CUP', required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Proceso",
                                 required=True, )
    active = fields.Boolean(string="Activo", default=True, )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El Centro de costo ya existe !"),
    ]
