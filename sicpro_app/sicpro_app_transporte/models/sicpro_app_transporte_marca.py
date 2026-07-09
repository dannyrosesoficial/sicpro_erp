# -*- coding: utf-8 -*-

from odoo import fields, models


class TransporteModeloBrand(models.Model):
    _name = 'sicpro.app.transporte.modelo'
    _description = 'Modelo de Transporte'
    _order = 'name asc'

    name = fields.Char('Modelo', required=True)
    image_128 = fields.Image("Logo", max_width=128, max_height=128)
