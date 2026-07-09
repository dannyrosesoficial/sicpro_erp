# -*- coding: utf-8 -*-

from odoo import api, fields, models


class TrabajadoresSeguridadProteccion(models.Model):
    _name = 'sicpro.app.trabajadores.seguridad.proteccion'
    _description = 'Tipo de Modulo de Seguridad para los trabajadores'
    _order = "name asc"

    codigo = fields.Char(string='Código', required=True)
    name = fields.Char(string='Descripción', required=True)
    vida_util = fields.Char(string='Vida Util', required=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    precio = fields.Monetary("Precio", currency_field='company_currency_id',
                             required=True)
    unida_medida = fields.Char(string='Unidad de Medidas', required=True)

    cantidad = fields.Integer(string='Cantidad', required=True)
    cargo = fields.Many2one('sicpro.app.trabajadores.cargos',
                            string="Cargo Asociado", required=True, )


