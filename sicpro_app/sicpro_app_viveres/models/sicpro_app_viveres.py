# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import datetime


class Viveres(models.Model):
    _name = 'sicpro.app.viveres'
    _description = "Control entrega de víveres"

    name = fields.Many2one('sicpro.app.viveres.productos.comprados', string='Producto', required=True)
    numero_entrega = fields.Integer('Número de entrega', related='name.numero', store=True)
    fecha = fields.Date('Fecha compra', related='name.fecha', store=True)
    precio = fields.Monetary('Precio', currency_field='company_currency', required=True)
    total_trabajadores = fields.Integer('Total entregados', compute='_compute_total_trabajadores')
    active = fields.Boolean('Activo', default=True)
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Currency', readonly=True, related='company_id.currency_id')

    def _compute_total_trabajadores(self):
        for each in self:
            area_entregas = self.env['sicpro.app.viveres.areas.entregas'].search(
                [('producto_comprado', '=', each.name.id)])

            for area in area_entregas:
                each.total_trabajadores += area.total_entregado
