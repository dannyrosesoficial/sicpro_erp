# -*- coding: utf-8 -*-

from odoo import fields, models


class OrdenesClasesProyectos(models.Model):
    _name = 'sicpro.app.ordenes.clases.proyecto'
    _description = 'Clase de trabajo para las órdenes de proyecto'

    name = fields.Char('Clase', required=True)
    nombre = fields.Char('Nombre', required=True)
    control_autor = fields.Boolean(string='Control de autor', required=False, default=False)
    active = fields.Boolean('Activo', default=True)
