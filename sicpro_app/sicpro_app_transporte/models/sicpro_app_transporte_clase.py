# -*- coding: utf-8 -*-

from odoo import fields, models


class TransporteClase(models.Model):
    _name = 'sicpro.app.transporte.clase'
    _description = 'Clase del vehículo'
    _order = 'name asc'

    name = fields.Char('Clase', required=True,)
    active = fields.Boolean(string="Activo", default=True, )
