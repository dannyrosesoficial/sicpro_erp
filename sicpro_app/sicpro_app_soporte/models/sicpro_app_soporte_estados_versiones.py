# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class SoporteEstadosVersiones(models.Model):
    _name = 'sicpro.app.soporte.estados.versiones'
    _description = 'Estados de las versiones del sistema'
    _order = 'sequence, id'

    name = fields.Char(string='Estado', required=True)
    descripcion = fields.Text(string='Descripción')
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    inicial = fields.Boolean(string='Estado Desarrollo')
    closed = fields.Boolean(string='Estado Final')
    fold = fields.Boolean(string='Solapado en Kanban')
