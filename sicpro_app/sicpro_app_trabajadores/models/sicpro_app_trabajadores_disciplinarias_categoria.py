# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class TrabajadoresCategoriasDisiplinarias(models.Model):
    _name = 'sicpro.app.trabajadores.disiplinaria.categorias'
    _description = 'Categorías de medidas disciplinarias'

    code = fields.Char(string="Código", required=True)
    name = fields.Char(string="Nombre", required=True)
    vigencia = fields.Integer(string="Vigencia (Días)", required=True)
    category_type = fields.Selection(
        [('disciplinary', 'Categoría Disciplinaria'),
         ('action', 'Categoría Acciones')], string="Categoría")
    description = fields.Text(string="Detalles")



