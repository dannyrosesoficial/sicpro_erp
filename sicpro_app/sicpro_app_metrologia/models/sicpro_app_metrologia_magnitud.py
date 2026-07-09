# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api


class MetrologiaMagnitudes(models.Model):
    _name = 'sicpro.app.metrologia.magnitud'
    _description = 'Magnitudes de la Metrología'

    name = fields.Char(string="Magnitud", required=True, )
    magnitud_corta = fields.Char(string="Abreviatura", required=False, )
    active = fields.Boolean(string='Activo', default=True, index=True)
    vigencia = fields.Integer(string='Vigencia (Años)', required=True)
    dias = fields.Integer(string='Días', required=True,
                          compute='_compute_dias_vigencia')

    @api.depends('vigencia')
    def _compute_dias_vigencia(self):
        for item in self:
            if item.vigencia != 0:
                item.dias = item.vigencia * 365
            else:
                item.dias = 0
