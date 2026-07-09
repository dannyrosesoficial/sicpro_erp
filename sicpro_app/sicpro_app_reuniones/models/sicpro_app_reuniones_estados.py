# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class ReunionesEstados(models.Model):
    _name = 'sicpro.app.reuniones.estados'
    _description = 'Estados de las Reuniones'
    _order = 'sequence, name'

    name = fields.Char(string='Nombre del estado', required=True)
    description = fields.Text(string='Descripción del estado')
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    fold = fields.Boolean(string='Solapado en kanban', default=False)
    pipe_end = fields.Boolean(string='Estado final', default=False)
