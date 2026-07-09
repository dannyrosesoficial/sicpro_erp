# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class EstadosTerritorios(models.Model):
    _name = 'sicpro.nomenclador.territorios'
    _description = 'Nomenclador de Unidades Organizativa'

    name = fields.Char(required=True, string='Unidad Organizativa')
    codigo = fields.Integer(string="Código", required=True)
    abreviatura = fields.Char(required=True, string='Abreviatura')
    provincias_id = fields.Many2one(comodel_name="res.country.state",
                                    string="Provincia", required=True)
    active = fields.Boolean(string="Activo", default=True, index=True)
