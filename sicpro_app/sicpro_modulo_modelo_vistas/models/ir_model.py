# -*- coding: utf-8 -*--

from odoo import models


class IrModel(models.Model):
    _inherit = "ir.model"

    def action_show_records(self):
        for model in self:
            return {
                "display_name": model.name,
                "name": model.name,
                "type": "ir.actions.act_window",
                "view_type": "form",
                "view_mode": "tree,form",
                "res_model": model.model,
                "views": [],
                "view_id": [],
                "target": "current",
                "context": self._context,
            }
