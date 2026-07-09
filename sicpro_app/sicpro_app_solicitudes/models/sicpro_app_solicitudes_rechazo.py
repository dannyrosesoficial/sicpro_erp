# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class SolicitudesRechazadas(models.Model):
    _name = 'sicpro.app.solicitudes.rechazadas'
    _description = 'Motivo de rechazo'

    name = fields.Char(string='Descripción', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
