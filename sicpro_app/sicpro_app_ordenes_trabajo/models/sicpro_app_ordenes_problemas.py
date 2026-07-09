# -*- coding: utf-8 -*-

from odoo import fields, models


class OrdenesProblemas(models.Model):
    _name = 'sicpro.app.ordenes.problemas'
    _description = 'Problemas en la ejecución'

    name = fields.Char('Descripción', required=True)
    active = fields.Boolean('Activo', default=True)
