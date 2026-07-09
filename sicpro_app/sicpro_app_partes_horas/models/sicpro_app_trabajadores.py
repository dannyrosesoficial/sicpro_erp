# -*- coding: utf-8 -*-

from odoo import fields, models


class Trabajadores(models.Model):
    _inherit = 'sicpro.app.trabajadores.general'

    costo = fields.Monetary(
        'Coste del parte de horas', currency_field='currency_id',
        groups="sicpro_app_trabajadores.grupo_app_trabajadores_usuario",
        default=0.0)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id',
                                  readonly=True)
