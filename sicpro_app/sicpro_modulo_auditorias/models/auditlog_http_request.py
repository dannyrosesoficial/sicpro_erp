# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from psycopg2.extensions import AsIs

from odoo import api, fields, models
from odoo.http import request


class AuditlogHTTPRequest(models.Model):
    _name = "auditlog.http.request"
    _description = "Registro de auditoría: registro de solicitudes HTTP"
    _order = "create_date DESC"

    display_name = fields.Char(string="Nombre", compute="_compute_display_name",
                               store=True)
    name = fields.Char(string="Ruta")
    root_url = fields.Char(string="URL raíz")
    user_id = fields.Many2one("res.users", string="Usuario")
    http_session_id = fields.Many2one("auditlog.http.session", string="Sesión",
                                      index=True)
    user_context = fields.Char(string="Contexto")
    log_ids = fields.One2many("auditlog.log", "http_request_id", string="Logs")

    @api.depends("create_date", "name")
    def _compute_display_name(self):
        for httprequest in self:
            create_date = (fields.Datetime.from_string(
                httprequest.create_date) or fields.Datetime.now())
            tz_create_date = fields.Datetime.context_timestamp(httprequest,
                                                               create_date)
            httprequest.display_name = "{} ({})".format(
                httprequest.name or "?",
                fields.Datetime.to_string(tz_create_date))

    @api.model
    def current_http_request(self):
        if not request:
            return False
        http_session_model = self.env["auditlog.http.session"]
        httprequest = request.httprequest
        if httprequest:
            if hasattr(httprequest, "auditlog_http_request_id"):
                # Verificar existencia. Podría haberse revertido después de un
                # error de simultaneidad
                self.env.cr.execute("SELECT id FROM %s WHERE id = %s", (
                AsIs(self._table), httprequest.auditlog_http_request_id), )
                if self.env.cr.fetchone():
                    return httprequest.auditlog_http_request_id
            vals = {"name": httprequest.path, "root_url": httprequest.url_root,
                "user_id": request.env.uid,
                "http_session_id": http_session_model.current_http_session(),
                "user_context": request.env.context, }
            httprequest.auditlog_http_request_id = self.create(vals).id
            return httprequest.auditlog_http_request_id
        return False
