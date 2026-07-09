# -*- coding: utf-8 -*-

from odoo import fields, models


class DashboardExtendidoIdentificador(models.Model):
    _inherit = 'sicpro.modulo.dashboard.tableros'

    identificador_tablero = fields.Selection(
        selection_add=[('sicpro.app.metrologia', 'Dashboard de Metrología')],
        ondelete={'sicpro.app.metrologia': 'cascade'})
