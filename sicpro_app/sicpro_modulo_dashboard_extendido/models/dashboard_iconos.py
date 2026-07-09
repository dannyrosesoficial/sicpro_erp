# -*- coding: utf-8 -*-

from odoo import models, fields


class IconosConfig(models.Model):
    _name = 'sicpro.modulo.dashboard.iconos'
    _description = 'Nomenclador de Íconos'

    name = fields.Char(required=True, string='Nombre')
    clase = fields.Char(required=True, string='Clase')
    icono = fields.Char(string='Ícono')
    active = fields.Boolean(string="Activo", default=True)
