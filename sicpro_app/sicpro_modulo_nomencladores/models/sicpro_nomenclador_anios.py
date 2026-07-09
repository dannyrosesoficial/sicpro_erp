# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NomencladorAnios(models.Model):
    _name = 'sicpro.nomenclador.anios'
    _description = 'Nomenclador de Años'

    name = fields.Char(required=True, string='Años')
    active = fields.Boolean(string="Activo", default=True, )
