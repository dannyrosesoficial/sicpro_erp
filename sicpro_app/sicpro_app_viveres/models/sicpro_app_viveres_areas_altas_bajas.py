# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class ViveresAreasAltasBajas(models.Model):
    _name = 'sicpro.app.viveres.areas.altas.bajas'
    _description = "Altas y bajas mensuales por áreas, módulo de víveres"

    name = fields.Many2one('sicpro.app.viveres.areas', string='Área', )
    direccion = fields.Many2one('res.company', string='Dirección',
                                related='name.direccion', store=True, )
    active = fields.Boolean(string='Activo', default=True, index=True)
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses',
                          string='Mes', required=True)
    anio = fields.Char(string='Año', required=True,
                       default=fields.Datetime.now().strftime("%Y"))
    trabajador = fields.Many2one('sicpro.app.trabajadores', 'Trabajador')
    estado = fields.Selection(selection=[('alta', 'Alta'), ('baja', 'Baja')],
                              string='Estado', )
    fecha = fields.Date(string='Fecha')
