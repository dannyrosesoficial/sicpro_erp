# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models, fields

class SicproLogSeverity(models.Model):
    _name = 'sicpro.log.severity'
    _description = 'Mapeo de Severidad'

    name = fields.Char(string="Nivel", required=True)
    code = fields.Char(string="Código", required=True)
    color = fields.Integer(string="Color (UI)")
    regex_pattern = fields.Char(string="Patrón Regex", required=True,
                                help="Patrón para identificar este nivel en texto.")