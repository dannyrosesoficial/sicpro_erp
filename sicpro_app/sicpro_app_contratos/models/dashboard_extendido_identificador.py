# -*- coding: utf-8 -*-

from odoo import fields, models


class DashboardExtendidoIdentificador(models.Model):
    _inherit = 'sicpro.modulo.dashboard.tableros'

    identificador_tablero = fields.Selection(
        selection_add=[('sicpro.app.contratos', 'Dashboard de Contratación')],
        ondelete={'sicpro.app.contratos': 'cascade'})
