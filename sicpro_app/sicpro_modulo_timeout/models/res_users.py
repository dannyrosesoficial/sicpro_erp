# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging
from os import utime
from os.path import getmtime
from time import time

from odoo import api, http, models
from odoo.http import SessionExpiredException

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _auth_timeout_get_ignored_urls(self):
        """Método conectable para calcular URL ignoradas
        El valor predeterminado es el parámetro de configuración almacenado
        """
        params = self.env["ir.config_parameter"]
        return params._auth_timeout_get_parameter_ignored_urls()

    @api.model
    def _auth_timeout_deadline_calculate(self):
        """Método conectable para calcular la fecha límite de tiempo de espera
        El valor predeterminado es la hora actual menos el retraso usando
        el retraso almacenado como configuración
        parámetro.
        """
        params = self.env["ir.config_parameter"]
        delay = params._auth_timeout_get_parameter_delay()
        if delay <= 0:
            return False
        return time() - delay

    @api.model
    def _auth_timeout_session_terminate(self, session):
        """Método conectable para finalizar una sesión agotada

        Esta es una etapa tardía en la que se puede cancelar el tiempo de
        espera de una sesión. Útil si desea realizar comprobaciones
        exhaustivas, ya que no será convocada a menos que se haya alcanzado la
         fecha límite de inactividad de la sesión.

        Retorno:
            Verdadero: sesión terminada
            Falso: tiempo de espera de sesión cancelado
        """
        if session.db and session.uid:
            session.logout(keep_db=True)
        return True

    @api.model
    def _auth_timeout_check(self):
        """Realice la validación del tiempo de espera de la sesión y caduque
         si es necesario."""

        if not http.request:
            return

        session = http.request.session

        # Calcular plazo
        deadline = self._auth_timeout_deadline_calculate()

        # Comprobar si se ha pasado el plazo
        expired = False
        if deadline is not False:
            path = http.root.session_store.get_session_filename(session.sid)
            try:
                expired = getmtime(path) < deadline
            except OSError:
                _logger.exception(
                    "Hora de modificación del archivo de sesión de lectura de excepción.", )
                # Forzar la caducidad de la sesión. Se resolverá con nueva sesión.
                expired = True

        # Intenta terminar la sesión.
        terminated = False
        if expired:
            terminated = self._auth_timeout_session_terminate(session)

        # Si la sesión terminó, acción terminada
        if terminated:
            return SessionExpiredException("La sesión expiró")

        # De lo contrario, actualice condicionalmente la sesión modificada y
        # los tiempos de acceso.
        ignored_urls = self._auth_timeout_get_ignored_urls()

        if http.request.httprequest.path not in ignored_urls:
            if "path" not in locals():
                path = http.root.session_store.get_session_filename(
                    session.sid, )
            try:
                utime(path, None)
            except OSError:
                _logger.exception(
                    "Excepción al actualizar el acceso al archivo de sesión/horas de modificación.", )
