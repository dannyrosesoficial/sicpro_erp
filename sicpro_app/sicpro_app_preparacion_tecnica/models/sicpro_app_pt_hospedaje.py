# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PreparacionTecnicaHospedaje(models.Model):
    _name = 'sicpro.app.preparacion.tecnica.hospedaje'
    _description = 'Hospedaje de la Preparación Técnica'

    preparaciones_id = fields.Many2one(
        comodel_name="sicpro.app.preparacion.tecnica.preparaciones",
        string="Preparaciones", ondelete="cascade", required=True, )
    provincia = fields.Many2one(
        string="Provincia", comodel_name="sicpro.nomenclador.provincia",
        required=True, )
    hospedaje = fields.Many2one(
        string="Hospedaje", comodel_name="sicpro.nomenclador.hospedaje",
        required=True, )
    gasto = fields.Monetary("Gasto", currency_field='company_currency_id',
                            related='hospedaje.valor', store=True, )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    observaciones = fields.Char(string='Observaciones', required=False)
