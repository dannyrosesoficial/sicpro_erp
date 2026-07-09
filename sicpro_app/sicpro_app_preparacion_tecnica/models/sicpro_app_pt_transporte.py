# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PreparacionTecnicaTransporte(models.Model):
    _name = 'sicpro.app.preparacion.tecnica.transporte'
    _description = 'Transporte de la Preparación Técnica'

    preparaciones_id = fields.Many2one(
        comodel_name="sicpro.app.preparacion.tecnica.preparaciones",
        string="Preparaciones", ondelete="cascade", required=True, )
    transporte_id = fields.Many2one(
        comodel_name="sicpro.app.transporte.general", string="Transporte",
        required=True, domain=[('active', '=', True)], )
    combustible = fields.Many2one(
        comodel_name="sicpro.app.transporte.tipo.combustible",
        string="Combustible", compute='_compute_combustible',
        compute_sudo=True, store=True, )
    cantidad_km = fields.Float(string="Cantidad Km", required=True)
    indice_consumo = fields.Float('Indice consumo',
                                  compute='_compute_indice_consumo',
                                  compute_sudo=True, store=True, )
    litros = fields.Float(
        'Litros', compute='_compute_litros', compute_sudo=True,
        store=True, )
    precio = fields.Float(string="Precio", compute='_compute_precio',
                          compute_sudo=True, store=True, )
    tag_ids = fields.Many2many('sicpro.app.transporte.etiqueta',
                               'sicpro_app_preparacion_tecnica_vehicle_rel',
                               'vehicle_tag_id', 'tag_id', 'Etiquetas',
                               compute='_compute_tag_ids', compute_sudo=True,
                               store=True, )
    presupuesto = fields.Monetary(
        "Presupuesto", compute='_compute_presupuesto', compute_sudo=True,
        store=True, currency_field='company_currency_id')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)

    # devuelve el tipo del combustible
    @api.depends('transporte_id')
    def _compute_combustible(self, ):
        for data in self:
            data.combustible = data.transporte_id.combustible

    # devuelve el valor del indice de consumo del vehículo
    @api.depends('transporte_id')
    def _compute_indice_consumo(self, ):
        for data in self:
            data.indice_consumo = data.transporte_id.indice_consumo_real

    # devuelve el valor del precio
    @api.depends('transporte_id')
    def _compute_precio(self, ):
        for data in self:
            data.precio = data.transporte_id.combustible.precio

    # devuelve el valor en litros
    @api.model
    @api.depends('cantidad_km')
    def _compute_litros(self, ):
        for data in self:
            if data.cantidad_km:
                data.litros = data.cantidad_km / data.indice_consumo

    # devuelve el valor de la etiqueta
    @api.depends('transporte_id')
    def _compute_tag_ids(self, ):
        for data in self:
            data.tag_ids = data.transporte_id.tag_ids

    # calculo el valor del presupuesto
    @api.depends('litros', 'precio')
    def _compute_presupuesto(self, ):
        for data in self:
            if data.litros:
                data.presupuesto = data.litros * data.precio

    @api.constrains("transporte_id")
    def _check_quantity(self, ):
        for transporte in self:
            if not transporte.cantidad_km > 0.0:
                raise ValidationError(
                    _("Quantity of material consumed must be greater than 0.")
                )