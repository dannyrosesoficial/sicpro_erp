# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class TrabajadoresCategoriasDisciplinarias(models.Model):
    _name = 'sicpro.app.trabajadores.disiplinaria.categorias'
    _description = 'Categorías de medidas disciplinarias'

    code = fields.Char(string="Código", required=True)
    name = fields.Char(string="Nombre", required=True)
    vigencia = fields.Integer(string="Vigencia (Días)", required=True)
    category_type = fields.Selection(
        [('disciplinary', 'Categoría Disciplinaria'),
         ('action', 'Categoría Acciones')], string="Categoría")
    description = fields.Text(string="Detalles")
