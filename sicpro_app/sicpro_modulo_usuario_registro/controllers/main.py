# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
import logging

from odoo import http, fields
from odoo.addons.web.controllers.session import Session
from odoo.http import request

_logger = logging.getLogger(__name__)


class SessionInherit(Session):

    @http.route()
    def logout(self, redirect='/sicpro'):
        uid = request.session.uid

        if uid:
            user = request.env['res.users'].sudo().browse(uid)

            if user.exists():
                user.status = 'blocked'

                record = request.env[
                    'sicpro.modulo.registro.usuarios'].sudo().search(
                    [('name', '=', user.id), ('logout_time', '=', False)],
                    limit=1, order='logout_time desc')

                if record:
                    record.logout_time = fields.Datetime.now()

                _logger.info("Cierre de sesión registrado para el usuario: %s",
                             user.login)

        return super(SessionInherit, self).logout(redirect=redirect)
