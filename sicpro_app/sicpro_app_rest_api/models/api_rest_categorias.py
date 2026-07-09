# -*- coding: utf-8 -*-


from odoo import fields, models


class ApiRestTag(models.Model):
    _name = 'api.rest.tag'
    _description = 'Categorías del Api Rest'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Char(string='Descripción')
