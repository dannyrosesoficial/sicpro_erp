# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class EstadosProblemasEjecucion(models.Model):
    _name = 'sicpro.nomenclador.problemas.ejecucion'
    _description = 'Nomenclador de Problemas en la Ejecución'

    name = fields.Char(required=True, string='Problemas')
    company_id = fields.Many2one(comodel_name="res.company", string="Proceso",
                                 required=True)
    active = fields.Boolean(string="Activo", default=True, index=True)
