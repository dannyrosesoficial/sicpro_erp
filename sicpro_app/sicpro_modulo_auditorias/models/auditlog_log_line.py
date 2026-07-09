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


class AuditlogLogLine(models.Model):
    _name = "auditlog.log.line"
    _description = "Registro de auditoría: detalles del registro (campos actualizados)"

    field_id = fields.Many2one("ir.model.fields", ondelete="set null",
                               index=True)
    log_id = fields.Many2one("auditlog.log", ondelete="cascade", index=True)
    old_value = fields.Text()
    new_value = fields.Text()
    old_value_text = fields.Text(string="Texto de valor antiguo")
    new_value_text = fields.Text(string="Nuevo valor Texto")
    field_name = fields.Char(string="Nombre técnico", readonly=True)
    field_description = fields.Char(string="Descripción", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("field_id"):
                raise UserError(
                    "No hay ningún campo definido para crear línea.")
            field = self.env["ir.model.fields"].sudo().browse(vals["field_id"])
            vals.update({"field_name": field.name,
                         "field_description": field.field_description})
        return super().create(vals_list)

    def write(self, vals):
        if "field_id" in vals:
            if not vals["field_id"]:
                raise UserError("El campo 'field_id' no puede estar vacío.")
            field = self.env["ir.model.fields"].sudo().browse(vals["field_id"])
            vals.update({"field_name": field.name,
                         "field_description": field.field_description})
        return super().write(vals)
