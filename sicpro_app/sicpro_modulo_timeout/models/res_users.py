# -*- coding: utf-8 -*-

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
        """Verifica las calcular URL ignoradas en los valores predeterminados
        de los parámetro de configuración almacenado
        """
        params = self.env["ir.config_parameter"]
        return params._auth_timeout_get_parameter_ignored_urls()

    @api.model
    def _auth_timeout_deadline_calculate(self):
        """Calcula la fecha límite de tiempo de espera predeterminado y la hora
         actual menos el retraso usando el retraso almacenado como
         configuración."""
        params = self.env["ir.config_parameter"]
        delay = params._auth_timeout_get_parameter_delay()
        if delay <= 0:
            return False
        return time() - delay

    @api.model
    def _auth_timeout_session_terminate(self, session):
        """Finaliza una sesión agotada, esta es una etapa tardía en la que se
        puede cancelar el tiempo de espera de una sesión.
        Útil si desea realizar una comprobación exhaustiva, ya que no será
        llamado a menos que se haya alcanzado la fecha límite de inactividad
        de la sesión.

        Return:
            True: session terminated
            False: session timeout cancelled
        """
        if session.db and session.uid:
            session.logout(keep_db=True)
        return True

    @api.model
    def _auth_timeout_check(self):
        """Realice la validación del tiempo de espera de la sesión y  la
        expira si es necesario."""
        if not http.request:
            return
        session = http.request.session

        # Calcular fecha límite
        deadline = self._auth_timeout_deadline_calculate()

        # Compruebe si ha pasado la fecha límite
        expired = False
        if deadline is not False:
            path = http.root.session_store.get_session_filename(session.sid)
            try:

                expired = getmtime(path) < deadline
            except Exception:
                # _logger.exception("Excepción modificación del archivo
                # de sesión de lectura.",)

                # Forzar la expiración de la sesión.
                # Se resolverá con nueva sesión..
                expired = True

        # Intenta terminar la sesión
        terminated = False
        if expired:
            terminated = self._auth_timeout_session_terminate(session)

        # Si la sesión terminó, todos listo
        if terminated:
            raise SessionExpiredException("La sesión del usuario ha expirado")

        # De lo contrario, actualice condicionalmente la sesión modificada y
        # los tiempos de acceso
        ignored_urls = self._auth_timeout_get_ignored_urls()

        if http.request.httprequest.path not in ignored_urls:
            if "path" not in locals():
                path = http.root.session_store.get_session_filename(
                    session.sid,
                )
            try:
                utime(path, None)
            except Exception:
                _logger.exception(
                    "Excepción de actualización de acceso a archivos de sesión"
                    "/ tiempos modificados.",
                )
