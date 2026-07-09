# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class SicproWebEvolution(models.Model):
    _name = 'sicpro.modulo.web.evolucion'
    _description = 'Hitos de Evolución SICPRO'
    _order = 'sequence, periodo desc'

    name = fields.Char(string='Título del Hito', required=True)
    subtitulo = fields.Char(string='Subtítulo')
    periodo = fields.Char(string='Periodo/Año')
    sequence = fields.Integer(string='Orden', default=1, index=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
