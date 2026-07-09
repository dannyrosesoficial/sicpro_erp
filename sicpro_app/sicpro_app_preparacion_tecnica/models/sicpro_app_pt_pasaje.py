# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PreparacionTecnicaPasaje(models.Model):
    _name = 'sicpro.app.preparacion.tecnica.pasaje'
    _description = 'Pasaje de la Preparación Técnica'

    preparaciones_id = fields.Many2one(
        comodel_name="sicpro.app.preparacion.tecnica.preparaciones",
        string="Preparaciones", ondelete="cascade", required=True, )
    provincia = fields.Many2one(
        string="Provincia", comodel_name="sicpro.nomenclador.provincia",
        required=True, )
    pasaje = fields.Many2one(
        string="Pasaje", comodel_name="sicpro.nomenclador.pasaje",
        required=True, )
    gasto = fields.Monetary("Gasto", currency_field='company_currency_id',
                            related='pasaje.valor', store=True, )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    tipo = fields.Selection(string='Tipo', selection=[
        ('ida', 'Ida'), ('vuelta', 'vuelta'), ], required=True, )
    observaciones = fields.Char(string='Observaciones', required=False)