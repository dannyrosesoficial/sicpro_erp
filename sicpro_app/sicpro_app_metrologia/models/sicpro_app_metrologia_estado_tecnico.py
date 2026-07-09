# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class MetrologiaEstadoTecnico(models.Model):
    _name = 'sicpro.app.metrologia.estado.tecnico'
    _order = 'sequence asc'
    _description = 'Estado Técnico Metrología'

    name = fields.Char(string="Estado Técnico", required=True, )
    active = fields.Boolean(string='Activo', default=True, index=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    fold = fields.Boolean(string='Plegado')
    laboratorio = fields.Boolean(string='En Laboratorio')
    sin_calibrar = fields.Boolean(string='Sin Calibrar')
    baja = fields.Boolean(string='Baja')
