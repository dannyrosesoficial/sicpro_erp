# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class ViveresAreasEfectivo(models.Model):
    _name = 'sicpro.app.viveres.areas.efectivo'
    _description = "Efectivo entregado por áreas, módulo de víveres"

    name = fields.Many2one('sicpro.app.viveres.areas', string='Área', required=True)
    direccion = fields.Many2one('res.company', string='Dirección', related='name.direccion', store=True, )
    active = fields.Boolean('Activo', default=True)
    fecha = fields.Date(string='Fecha entrega', required=True)
    total_trabajadores = fields.Integer('Total área', compute='_compute_total_trabajadores', readonly=True)
    total_entregado = fields.Integer('Total entregado', required=True)
    monto_individual_entregado = fields.Monetary('Monto individual', currency_field='company_currency', required=True)
    monto_total_entregado = fields.Monetary('Monto total', compute='_compute_monto_total_entregado', readonly=True,
                                            currency_field='company_currency')
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Currency', readonly=True, related='company_id.currency_id')
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses', string='Mes', )
    codigo_mes = fields.Integer(string="Código Mes", related='mes.codigo_mes')
    anio = fields.Char(string='Año', default=fields.Datetime.now().strftime("%Y"))

    @api.depends("name.name")
    def _compute_total_trabajadores(self):
        global area_totales
        hoy = datetime.today()
        mes_anterior, anio = (hoy.month - 1, hoy.year) if hoy.month != 1 else (12, hoy.year - 1)
        for each in self:
            if each:
                area_totales = self.env['sicpro.app.viveres.cierre'].search(
                    ['&', ('name', '=', each.name.id), ('codigo_mes', '=', mes_anterior), ('anio', '=', anio)])

            if area_totales:
                each.total_trabajadores = area_totales.total
            else:
                each.total_trabajadores = 0

    @api.depends('monto_individual_entregado', 'total_entregado')
    def _compute_monto_total_entregado(self):
        for each in self:
            each.monto_total_entregado = each.monto_individual_entregado * each.total_entregado

    @api.model
    def create(self, vals_list):
        res = super(ViveresAreasEfectivo, self).create(vals_list)

        nombre_mes = self.env['sicpro.nomenclador.meses'].search(
            ['&', ('active', '=', True), ('codigo_mes', '=', res['fecha'].month)])
        res['mes'] = nombre_mes.id
        res['anio'] = res['fecha'].year

        return res
