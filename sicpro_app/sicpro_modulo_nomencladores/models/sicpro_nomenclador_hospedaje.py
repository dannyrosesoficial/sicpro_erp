# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EstadosHospedaje(models.Model):
    _name = 'sicpro.nomenclador.hospedaje'
    _description = 'Hospedaje'

    name = fields.Char(required=True, string='Hospedaje')
    provincia = fields.Many2one(comodel_name="sicpro.nomenclador.provincia",
                                string="Provincia", required=True, )
    valor = fields.Monetary("Valor", currency_field='company_currency',
                            required=True)
    descripcion = fields.Char(string="Descripción", required=False, )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Currency',
                                       related='company_id.currency_id',
                                       readonly=True,
                                       relation="res.currency")
    active = fields.Boolean(string="Activo", default=True, )
