# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields

class SicproMultimediaTag(models.Model):
    _name = 'sicpro.multimedia.tag'
    _description = 'Etiquetas Multimedia'
    _order = 'name'

    name = fields.Char(string='Nombre de Etiqueta', required=True, translate=True)
    color = fields.Integer(string='Índice de Color', default=0)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', '¡El nombre de la etiqueta ya existe!'),
    ]
