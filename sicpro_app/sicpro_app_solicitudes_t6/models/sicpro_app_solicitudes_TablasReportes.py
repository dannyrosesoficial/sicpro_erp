# -*- coding: utf-8 -*-


from odoo import fields, models, api


class SolicitudesGenerales(models.Model):
    _inherit = ['sicpro.app.solicitudes.oportunidades']

    herencia_t6 = fields.Char()
    oportunidad_id = fields.Many2one(
        comodel_name="sicpro.app.solicitudes.oportunidades")

