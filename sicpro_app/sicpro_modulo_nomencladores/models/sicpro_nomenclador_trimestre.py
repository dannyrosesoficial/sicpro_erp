# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint
from odoo import models, fields, api


class EstadosTrimestres(models.Model):
    _name = 'sicpro.nomenclador.trimestre'
    _description = 'Nomenclador de Trimestres'

    @api.model
    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True, string='Trimestre')
    descripcion = fields.Char(string="Descripción", required=True)
    active = fields.Boolean(string="Activo", default=True, index=True)
    color = fields.Integer(string='Color',
                           default=_default_color)
