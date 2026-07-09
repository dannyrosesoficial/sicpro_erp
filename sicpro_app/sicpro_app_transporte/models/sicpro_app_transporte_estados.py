# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models


class TransporteEstados(models.Model):
    _name = 'sicpro.app.transporte.estado'
    _order = 'sequence, id'
    _description = 'Estados del transporte'

    name = fields.Char(string="Nombre", required=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
