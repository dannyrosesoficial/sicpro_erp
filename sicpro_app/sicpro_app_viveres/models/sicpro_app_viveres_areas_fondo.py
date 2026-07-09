# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from datetime import date

from odoo import models, fields


class ViveresAreasFondo(models.Model):
    _name = 'sicpro.app.viveres.areas.fondo'
    _description = "Fondo por áreas, módulo de víveres"

    name = fields.Many2one('sicpro.app.viveres.areas', string='Área', )
    direccion = fields.Many2one('res.company', string='Dirección',
                                related='name.direccion', store=True, )
    active = fields.Boolean(string='Activo', default=True, index=True)
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses',
                          string='Mes', )
    codigo_mes = fields.Integer(string="Código Mes", related='mes.codigo_mes')
    anio = fields.Char(string='Año',
                       default=fields.Datetime.now().strftime("%Y"))
    fondo = fields.Monetary(string='Fondo', compute='_compute_fondo', readonly=True,
                            currency_field='company_currency')
    fecha_entrega = fields.Date(string='Fecha última entrega efectivo',
                                compute='_compute_ultima_entrega',
                                readonly=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Moneda', readonly=True,
                                       related='company_id.currency_id')

    def _compute_fondo(self):
        for each in self:
            area_efectivos = self.env[
                'sicpro.app.viveres.areas.efectivo'].search(
                ['&', ('name', '=', each.name.id),
                 ('codigo_mes', '=', each.codigo_mes),
                 ('anio', '=', each.anio)])

            total_efectivo = 0
            for efectivo in area_efectivos:
                total_efectivo = efectivo.monto_total_entregado

            area_entregas = self.env[
                'sicpro.app.viveres.areas.entregas'].search(
                ['&', ('name', '=', each.name.id),
                 ('codigo_mes', '=', each.codigo_mes),
                 ('anio', '=', each.anio)])

            total_entrega = 0
            for entrega in area_entregas:
                for producto in entrega.producto_comprado:
                    total_entrega = producto.precio * entrega.total_entregado

            each.fondo = total_efectivo - total_entrega

    def _compute_ultima_entrega(self):
        for each in self:
            area_efectivos = self.env[
                'sicpro.app.viveres.areas.efectivo'].search(
                [('name', '=', each.name.id)])
            fecha = date(1990, 1, 1)
            for efectivo in area_efectivos:
                if efectivo.fecha >= fecha:
                    fecha = efectivo.fecha
            each.fecha_entrega = fecha if fecha != date(1990, 1, 1) else None
