# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import api, fields, models
from odoo.http import request


class AuditlogHTTPSession(models.Model):
    _name = "auditlog.http.session"
    _description = "Registro de auditoría: registro de sesión de usuario HTTP"
    _order = "create_date DESC"

    display_name = fields.Char(string="Nombre", compute="_compute_display_name",
        store=True)
    name = fields.Char(string="ID de sesión", index=True)
    user_id = fields.Many2one("res.users", string="Usurio", index=True)
    http_request_ids = fields.One2many("auditlog.http.request",
        "http_session_id", string="Solicitudes HTTP")

    @api.depends("create_date", "user_id")
    def _compute_display_name(self):
        for httpsession in self:
            create_date = (fields.Datetime.from_string(
                httpsession.create_date) or fields.Datetime.now())
            tz_create_date = fields.Datetime.context_timestamp(httpsession,
                create_date)
            httpsession.display_name = "{} ({})".format(
                httpsession.user_id and httpsession.user_id.name or "?",
                fields.Datetime.to_string(tz_create_date), )

    @api.model
    def current_http_session(self):
        if not request:
            return False
        httpsession = request.session
        if httpsession:
            existing_session = self.search([("name", "=", httpsession.sid),
                ("user_id", "=", request.env.uid), ], limit=1, )
            if existing_session:
                return existing_session.id
            vals = {"name": httpsession.sid, "user_id": request.env.uid}
            return self.create(vals).id
        return False
