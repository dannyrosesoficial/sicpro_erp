# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
from odoo import fields, models


class Survey(models.Model):
    _inherit = 'survey.survey'

    access_mode = fields.Selection(selection_add=[('website', 'Sitio Web')], ondelete={'website': 'cascade'})

    visibility = fields.Boolean(string='Visible en Portal', help="Visibilidad de esta encuesta en el portal.")

    def action_answer_report_download(self):
        """Genera la URL para la descarga del reporte en formato Excel (XLSX)."""
        return {'type': 'ir.actions.act_url', 'url': f'/xlsx_report/{self.id}', 'target': 'new', }