# -*- coding: utf-8 -*-

from odoo import models, fields


class NomencladorLocales(models.Model):
    _name = 'sicpro.nomenclador.locales'
    _description = 'Nomenclador de Locales de CC'
    _order = "id"

    name = fields.Char(required=True, string='Local')
    centro_costo = fields.Many2one(
        string='Centro Costo', required=True,
        comodel_name='sicpro.nomenclador.centro.costo', )
    descripcion = fields.Char(string='Descripción', required=False)
    company_id = fields.Many2one(comodel_name="res.company", string="Proceso",
                                 related='centro_costo.company_id', store=True,
                                 required=False, )
    active = fields.Boolean(string="Activo", default=True,)