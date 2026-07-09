# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class TrabajadoresLocales(models.Model):
    _name = 'sicpro.app.trabajadores.local'
    _description = 'Locales del trabajador'

    name = fields.Char(string="Local", required=False, )
    locales_id = fields.Char(required=False, )
