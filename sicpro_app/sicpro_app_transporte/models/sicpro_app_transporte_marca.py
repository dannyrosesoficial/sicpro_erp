# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class TransporteModeloBrand(models.Model):
    _name = 'sicpro.app.transporte.modelo'
    _description = 'Modelo de Transporte'
    _order = 'name asc'

    name = fields.Char(string='Modelo', required=True)
    image_128 = fields.Image("Logo", max_width=128, max_height=128)
