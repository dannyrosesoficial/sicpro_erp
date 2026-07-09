# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models


class AuditlogLogLineView(models.Model):
    _name = "auditlog.log.line.view"
    _inherit = "auditlog.log.line"
    _description = "Registro de auditoría: detalles del registro (campos actualizados)"
    _auto = False
    _log_access = True

    name = fields.Char()
    model_id = fields.Many2one("ir.model")
    model_name = fields.Char()
    model_model = fields.Char()
    res_id = fields.Integer()
    user_id = fields.Many2one("res.users")
    method = fields.Char()
    http_session_id = fields.Many2one("auditlog.http.session", string="Sesión",
        index=True)
    http_request_id = fields.Many2one("auditlog.http.request",
        string="Solicitud HTTP", index=True)
    log_type = fields.Selection(
        selection=lambda r: r.env["auditlog.rule"]._fields[
            "log_type"].selection, string="Tipo", )

    def _select_query(self):
        return """
            alogl.id,
            alogl.create_date,
            alogl.create_uid,
            alogl.write_uid,
            alogl.write_date,
            alogl.field_id,
            alogl.log_id,
            alogl.old_value,
            alogl.new_value,
            alogl.old_value_text,
            alogl.new_value_text,
            alogl.field_name,
            alogl.field_description,
            alog.name,
            alog.model_id,
            alog.model_name,
            alog.model_model,
            alog.res_id,
            alog.user_id,
            alog.method,
            alog.http_session_id,
            alog.http_request_id,
            alog.log_type
        """

    def _from_query(self):
        return """
            auditlog_log_line alogl
            JOIN auditlog_log alog ON alog.id = alogl.log_id
        """

    @property
    def _table_query(self):
        return f"SELECT {self._select_query()} FROM {self._from_query()}"
