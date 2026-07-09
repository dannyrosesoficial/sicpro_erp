# -*- coding: utf-8 -*-

from odoo import models, fields


class EstadosTerritorios(models.Model):
    _name = 'sicpro.nomenclador.territorios'
    _description = 'Territorios'

    name = fields.Char(required=True, string='Territorio')
    codigo = fields.Integer(string="Código", required=True, )
    abreviatura = fields.Char(required=True, string='Abreviatura')
    provincia = fields.Many2one(comodel_name="sicpro.nomenclador.provincia",
                                string="Provincia", required=True, )
    active = fields.Boolean(string="Activo", default=True, )
