# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SicproAdministracionCambios(models.Model):
    _name = 'sicpro.app.administracion.cambios'
    _description = 'Configuración de los cambios de la Aplicación'

    # Por defecto el id que funciona es el 1
    name = fields.Html(string='Cambios', required=False)





