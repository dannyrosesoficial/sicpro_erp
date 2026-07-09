# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
from odoo import models, fields


class SicproAdministracion(models.Model):
    _name = 'sicpro.app.administracion'
    _description = 'Aplicación para la administración de SICPRO ERP'

    name = fields.Char(string='Admin', default='ADMINISTRACIÓN')


