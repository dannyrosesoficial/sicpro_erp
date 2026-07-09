# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class SoporteEstadospaquetes(models.Model):
    _name = 'sicpro.app.soporte.estados.paquetes'
    _description = 'Estados de los paquetes del sistema'
    _order = 'sequence, id'

    name = fields.Char(string='Estado', required=True)
    descripcion = fields.Text(string='Descripción')
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    inicial = fields.Boolean(string='Estado inicial')
    closed = fields.Boolean(string='Estado final')
    fold = fields.Boolean(string='Solapado en Kanban')
