# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging
import odoo
from odoo import http
from odoo.addons.web.controllers.home import Home, ensure_db
from odoo.http import request

_logger = logging.getLogger(__name__)


class SicproHome(Home):

    @classmethod
    def _is_sicpro_installed(cls, db_name):
        """
        Verifica de forma atómica mediante consulta SQL directa en PostgreSQL si la base
        de datos especificada tiene instalado el módulo 'sicpro_modulo_web'.
        Utiliza 'odoo.sql_db.db_connect' para evitar acoplamientos con el registro ORM,
        caché de entorno o fallos por contextos desalineados en 'request.env'.
        """
        if not db_name:
            return False
        try:
            if not odoo.service.db.exp_db_exist(db_name):
                return False
            db = odoo.sql_db.db_connect(db_name)
            with db.cursor() as cr:
                cr.execute(
                    "SELECT 1 FROM ir_module_module WHERE name = %s AND state = %s LIMIT 1",
                    ('sicpro_modulo_web', 'installed')
                )
                res = cr.fetchone()
                return bool(res)
        except Exception as error_check:
            _logger.warning("SICPRO ERP: Error SQL al verificar instalación de sicpro_modulo_web en BD '%s': %s", db_name, str(error_check))
            return False

    # 1. Página de inicio personalizada corporativa (Ruta aislada bajo /sicpro/inicio)
    @http.route('/sicpro/inicio', type='http', auth="public", website=True, sitemap=False, samesite='Lax')
    def web_inicio(self, **kwargs):
        """
        Renderiza la plantilla de portada/inicio corporativo para SICPRO ERP.
        Sincroniza el argumento 'db' de la URL si se accede directamente desde el selector.
        Si la BD activa no posee el módulo 'sicpro_modulo_web', redirige limpiamente a la entrada nativa de Odoo.
        """
        target_db = kwargs.get('db') or request.params.get('db')
        if target_db:
            request.session.db = target_db

        try:
            ensure_db()
        except Exception as error_db:
            _logger.warning("SICPRO ERP: No se pudo asegurar la base de datos en web_inicio: %s", str(error_db))
            return request.redirect('/web/database/selector')

        active_db = request.session.db

        # Verificación de alta velocidad por SQL directo a la BD activa
        modulo_sicpro_instalado = self._is_sicpro_installed(active_db)

        # Si la base de datos activa no posee SICPRO ERP, limpia la URL redirigiendo al backend o login nativo
        if not modulo_sicpro_instalado:
            _logger.info("SICPRO ERP: Petición a /sicpro/inicio en BD sin módulo '%s'. Redirigiendo a entrada nativa.", active_db)
            dest = '/web' if request.session.uid else '/web/login'
            return request.redirect(dest, code=303)

        return request.render("sicpro_modulo_web.web_plantilla_inicio", {})

    # 2. Interceptor principal del cliente web (Selección de BD en un solo clic y compatibilidad OWL/RPC)
    @http.route(
        ['/web', '/sicpro', '/odoo', '/odoo/<path:subpath>', '/scoped_app/<path:subpath>', '/'],
        type='http',
        auth="none",
        samesite='Lax'
    )
    def web_client(self, s_action=None, **kw):
        """
        Punto de entrada general optimizado para selección de bases de datos de un solo clic.
        Sincroniza dinámicamente 'request.session.db' con el argumento 'db' de la URL antes
        de llamar a 'ensure_db()', evitando rebotar al selector al cambiar entre BDs.
        """
        # A. Extracción y sincronización previa del parámetro 'db' enviado por el selector de Odoo
        target_db = kw.get('db') or request.params.get('db')
        if target_db:
            request.session.db = target_db

        # B. Comprobación segura de existencia de la base de datos seleccionada usando exp_db_exist
        if request.session.db:
            try:
                db_existe = odoo.service.db.exp_db_exist(request.session.db)
                if not db_existe:
                    _logger.warning("SICPRO ERP: La base de datos '%s' no existe en PostgreSQL.", request.session.db)
                    request.session.logout(keep_db=False)
                    return request.redirect('/web/database/selector')
            except Exception as error_exp:
                _logger.warning("SICPRO ERP: Error al verificar la base de datos '%s': %s", request.session.db, str(error_exp))
                request.session.logout(keep_db=False)
                return request.redirect('/web/database/selector')

        # C. Asegurar base de datos activa en el contexto de la petición
        try:
            ensure_db()
        except Exception as e_db:
            _logger.info("SICPRO ERP: Sin contexto de BD válido en la petición: %s. Redirigiendo al selector.", str(e_db))
            return request.redirect('/web/database/selector')

        # D. Inspección de la ruta solicitada para evitar interceptar estáticos o la portada
        current_path = request.httprequest.path or ''

        # E. Evaluación de sesión no autenticada para peticiones HTTP GET
        if not request.session.uid and request.httprequest.method == 'GET':
            # Evitar interceptar el portal corporativo o la pantalla de login nativa/custom
            rutas_excluidas = ['/sicpro/inicio', '/sicpro/inicio/', '/web/login', '/web/login/']
            if current_path not in rutas_excluidas:
                # Excluir de la redirección a los bundles de JS/CSS, imágenes estáticas, RPCs y websockets
                if not current_path.startswith(('/web/assets', '/web/content', '/web/static', '/web/dataset', '/websocket')):
                    # Validación aislada directa por SQL contra PostgreSQL
                    modulo_sicpro_instalado = self._is_sicpro_installed(request.session.db)

                    # Si la BD activa contiene el ecosistema SICPRO ERP instalado, redirige a su portada /sicpro/inicio
                    if modulo_sicpro_instalado:
                        return request.redirect('/sicpro/inicio', 303)

                    # Si es una base de datos limpia/estándar (sin sicpro_app_*), no se realiza redirección a /sicpro/inicio
                    # para evitar el 404. Se deja fluir el código hacia super().web_client() que renderizará /web/login nativo.

        # F. Delegación al método web_client nativo de Odoo 19 para mantener la interfaz OWL
        return super(SicproHome, self).web_client(s_action=s_action, **kw)

    # 3. Alineación del redireccionamiento tras el inicio de sesión
    def _login_redirect(self, uid, redirect=None):
        """
        Redirige a la ruta corporativa '/sicpro' si no viene un parámetro de redirección explícito,
        siempre que la base de datos activa cuente con el módulo 'sicpro_modulo_web'.
        En bases de datos limpias/estándar, redirige al backend nativo '/web'.
        """
        if not redirect or redirect in ['/', '/web', '/odoo']:
            active_db = request.session.db
            modulo_sicpro_instalado = self._is_sicpro_installed(active_db)

            if modulo_sicpro_instalado:
                redirect = '/sicpro'
            else:
                redirect = '/web'

        return super(SicproHome, self)._login_redirect(uid, redirect=redirect)