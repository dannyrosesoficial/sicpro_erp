# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import logging
from datetime import datetime, timedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AuditlogAutovacuum(models.TransientModel):
    _name = "auditlog.autovacuum"
    _description = "Registro de auditoría: eliminar registros antiguos"

    @api.model
    def autovacuum(self, days, chunk_size=None):
        """Elimine todos los registros con más de ``días``. Esto incluye:
            - Registros CRUD (crear, leer, escribir, desvincular)
            - solicitudes HTTP
            - Sesiones de usuario HTTP

        Llamado desde un cron.
        """
        days = (days > 0) and int(days) or 0
        deadline = datetime.now() - timedelta(days=days)
        data_models = ("auditlog.log", "auditlog.http.request", "auditlog.http.session")
        for data_model in data_models:
            records = self.env[data_model].search(
                [("create_date", "<=", fields.Datetime.to_string(deadline))],
                limit=chunk_size,
                order="create_date asc",
            )
            nb_records = len(records)
            records.unlink()
            _logger.info("AUTOVACUUM - %s '%s' registros eliminados", nb_records, data_model)
        return True
