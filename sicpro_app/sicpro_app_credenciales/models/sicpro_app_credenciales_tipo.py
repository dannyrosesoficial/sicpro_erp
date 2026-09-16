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


class CredencialesTipo(models.Model):
    _name = 'sicpro.app.credenciales.tipo'
    _description = "Tipo de Credenciales"
    _order = 'name'

    @api.model
    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Tipo", required=True)
    personal_externo = fields.Boolean(string='Personal Externo', required=False)
    color = fields.Integer(string='Color',
                           default=_default_color)
