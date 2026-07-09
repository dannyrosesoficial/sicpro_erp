# -*- coding: utf-8 -*-

from odoo import fields, models


class OrdenesParalizacion(models.Model):
    _name = 'sicpro.app.ordenes.paralizacion'
    _description = 'Motivo de la última paralización'

    name = fields.Char('Motivo', required=True)
    active = fields.Boolean('Activo', default=True)
