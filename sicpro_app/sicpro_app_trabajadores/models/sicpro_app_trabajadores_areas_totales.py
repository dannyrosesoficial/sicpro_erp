# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class TrabajadoresAreasTotales(models.Model):
    _name = 'sicpro.app.trabajadores.areas.totales'
    _description = "Totales mensuales por áreas, módulo de trabajadores"

    name = fields.Many2one('sicpro.app.trabajadores.areas', string='Área', )
    direccion = fields.Many2one('res.company', string='Proceso',
                                related='name.company_id', store=True, )
    active = fields.Boolean(string='Activo', default=True, index=True)
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses',
                          string='Mes', )
    codigo_mes = fields.Integer(string="Código Mes", related='mes.codigo_mes')
    anio = fields.Char(string='Año',
                       default=fields.Datetime.now().strftime("%Y"))
    total = fields.Integer(string='Total')
    estado = fields.Selection(
        selection=[('ok', 'Correcto'), ('error', 'Error')], string='Estado',
        default='ok')
