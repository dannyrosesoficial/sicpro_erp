# -*- coding: utf-8 -*-

from odoo import fields, models, _


class SicproMapas(models.Model):
    _name = 'sicpro.modulo.mapas'
    _description = "Registro de Plantillas de los Mapas"

    name = fields.Char('Nombre', translate=True, required=True)
    model_name = fields.Char('Nombre del Modelo', required=True)
    overlay_template = fields.Text('Plantilla', required=True)
    is_default = fields.Boolean(string="Por defecto", default=False)
