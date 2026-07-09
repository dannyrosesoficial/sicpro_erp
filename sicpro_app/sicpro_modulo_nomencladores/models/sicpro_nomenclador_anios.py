# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class NomencladorAnios(models.Model):
    _name = 'sicpro.nomenclador.anios'
    _description = 'Nomenclador de Años'

    name = fields.Char(required=True, string='Años')
    active = fields.Boolean(string="Activo", default=True, index=True)
