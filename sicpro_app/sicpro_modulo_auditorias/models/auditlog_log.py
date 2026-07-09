# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class AuditlogLog(models.Model):
    _name = "auditlog.log"
    _description = "Registro de auditoría - Registro"
    _order = "create_date desc"

    name = fields.Char(string="Nombre del recurso", size=64)
    model_id = fields.Many2one("ir.model", string="Model", index=True,
        ondelete="set null")
    model_name = fields.Char(readonly=True)
    model_model = fields.Char(string="Nombre del modelo técnico",
                              readonly=True)
    res_id = fields.Integer(string="ID de recurso")
    res_ids = fields.Char(string="ID de recursos")
    user_id = fields.Many2one("res.users", string="Usuario")
    method = fields.Char(size=64)
    line_ids = fields.One2many("auditlog.log.line", "log_id",
                               string="Campos actualizados")
    http_session_id = fields.Many2one("auditlog.http.session", string="Sesión",
                                      index=True)
    http_request_id = fields.Many2one("auditlog.http.request",
                                      string="Solicitud HTTP", index=True)
    log_type = fields.Selection(
        [("full", "Registro completo"), ("fast", "Registro rápido")],
        string="Tipo")

    @api.model_create_multi
    def create(self, vals_list):
        """Inserte los valores de los campos model_name y model_model al momento de la creación."""

        for vals in vals_list:
            if not vals.get("model_id"):
                raise UserError(
                    "No hay ningún modelo definido para crear el registro.")
            model = self.env["ir.model"].sudo().browse(vals["model_id"])
            vals.update({"model_name": model.name, "model_model": model.model})
        return super().create(vals_list)

    def write(self, vals):
        if "model_id" in vals:
            if not vals["model_id"]:
                raise UserError("El campo 'model_id' no puede estar vacío.")
            model = self.env["ir.model"].sudo().browse(vals["model_id"])
            vals.update({"model_name": model.name, "model_model": model.model})
        return super().write(vals)

    def show_res_ids(self):
        self.ensure_one()
        return {"type": "ir.actions.act_window", "view_mode": "list,form",
            "res_model": self.model_id.model,
            "domain": [("id", "in", safe_eval(self.res_ids))],
            "name": "Registros exportados", }
