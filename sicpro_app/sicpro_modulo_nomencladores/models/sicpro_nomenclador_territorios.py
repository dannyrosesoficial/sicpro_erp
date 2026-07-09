# -*- coding: utf-8 -*-

from odoo import models, fields


class EstadosTerritorios(models.Model):
    _name = 'sicpro.nomenclador.territorios'
    _description = 'Nomenclador de Unidades Organizativa'

    name = fields.Char(required=True, string='Unidad Organizativa')
    codigo = fields.Integer(string="Código", required=True, )
    abreviatura = fields.Char(required=True, string='Abreviatura')
    provincias_id = fields.Many2one(comodel_name="res.country.state",
                                    string="Provincia", required=True, )
    active = fields.Boolean(string="Activo", default=True, )
