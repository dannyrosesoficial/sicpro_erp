# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################-

from odoo import models


class IrModel(models.Model):
    _inherit = "ir.model"

    def action_show_records(self):
        for model in self:
            return {"display_name": model.name, "name": model.name,
                "type": "ir.actions.act_window", "view_type": "form",
                "view_mode": "list,form", "res_model": model.model,
                "views": [], "view_id": [], "target": "current",
                "context": self.env.context, }
