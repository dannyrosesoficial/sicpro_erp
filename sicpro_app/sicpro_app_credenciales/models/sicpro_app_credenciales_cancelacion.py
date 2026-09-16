# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import api, fields, models
from random import randint


class CredencialesCancelacion(models.Model):
    _name = 'sicpro.app.credenciales.cancelacion'
    _description = "Motivo de cancelación de las Credenciales"
    _order = 'name'

    @api.model
    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Motivo", required=True)
    color = fields.Integer(string='Color',
                           default=_default_color)
