# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class Viveres(models.Model):
    _name = 'sicpro.app.viveres'
    _description = "Control entrega de víveres"

    name = fields.Many2one('sicpro.app.viveres.productos.comprados',
                           string='Producto', required=True)
    numero_entrega = fields.Integer(string='Número de entrega', related='name.numero',
                                    store=True)
    fecha = fields.Date(string='Fecha compra', related='name.fecha', store=True)
    precio = fields.Monetary(string='Precio', currency_field='company_currency',
                             required=True)
    total_trabajadores = fields.Integer(string='Total entregados',
                                        compute='_compute_total_trabajadores')
    active = fields.Boolean(string='Activo', default=True, index=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Moneda', readonly=True,
                                       related='company_id.currency_id')

    def _compute_total_trabajadores(self):
        for each in self:
            area_entregas = self.env[
                'sicpro.app.viveres.areas.entregas'].search(
                [('producto_comprado', '=', each.name.id)])

            for area in area_entregas:
                each.total_trabajadores += area.total_entregado
