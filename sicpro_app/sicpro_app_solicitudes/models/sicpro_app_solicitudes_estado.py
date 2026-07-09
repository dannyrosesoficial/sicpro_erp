# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class SolicitudesEstados(models.Model):
    _name = "sicpro.app.solicitudes.estados"
    _description = "Estado de Solicitudes"
    _order = "sequence, name, id"

    name = fields.Char(string='Nombre del estado', required=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    is_inicial = fields.Boolean(string='¿Etapa inicial?')
    is_won = fields.Boolean(string='¿Etapa Ganada?')
    is_detenido = fields.Boolean(string='¿Etapa Detenida?')
    is_cancelado = fields.Boolean(string='¿Etapa Cancelada?')
    is_orden = fields.Boolean(string='¿Etapa vinculada a la OT?')
    requirements = fields.Text(string='Requerimientos')
    fold = fields.Boolean(string='Replegado en la vista Kanban', index=True)