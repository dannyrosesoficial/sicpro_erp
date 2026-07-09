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
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.web.controllers.home import Home, SIGN_UP_REQUEST_PARAMS
from datetime import datetime

CREDENTIAL_PARAMS = ['login', 'password', 'type', 'db']
_logger = logging.getLogger(__name__)

# IMPORTANTE
# Uso: Si el modal da problemas, simplemente escribe en el navegador:
# http://tu-ip-o-dominio/web/login?access=help

class HomeSicpro(Home):

    @http.route(['/web/login', '/sicpro/login'], type='http', auth='none', readonly=False)
    def web_login(self, redirect=None, **kw):
        odoo.addons.web.controllers.utils.ensure_db()

        # --- LÓGICA DE MANTENIMIENTO DINÁMICO Danny Rose's  ---
        # Uso: Si el modal te da problemas, simplemente escribe en el navegador:
        # http://tu-ip-o-dominio/web/login?access=help
        is_help_url = kw.get('access') == 'help'
        maintenance_record = request.env[
            'sicpro.modulo.web.mantenimiento'].sudo().search([], limit=1)

        # Extraemos la lógica de preparación de valores para reutilizarla en caso de error
        def get_maintenance_values(error_msg=None):
            start_date_iso = datetime.now().isoformat()
            if maintenance_record.maintenance_start_date:
                start_date_iso = maintenance_record.maintenance_start_date.isoformat()

            vals = {
                'maintenance_time': maintenance_record.estimated_time or '00:00:00',
                'secret_pass': maintenance_record.maintenance_password or '',
                'start_date': start_date_iso,
                'databases': http.db_list() if odoo.tools.config[
                    'list_db'] else None, }
            if error_msg:
                vals['error'] = error_msg
                vals['login'] = request.params.get(
                    'login')  # Para que el usuario no se borre al fallar
            return vals

        # Si el mantenimiento está activo y NO es una petición de login (GET inicial)
        if maintenance_record and maintenance_record.active_maintenance and not is_help_url and request.httprequest.method == 'GET':
            response = request.render(
                'sicpro_modulo_web_login.sicpro_template_mantenimiento',
                get_maintenance_values())
            response.headers['Cache-Control'] = 'no-cache'
            return response
        # ---------------------------------------------------------------

        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        if request.env.uid is None:
            if request.session.uid is None:
                request.env["ir.http"]._auth_method_public()
            else:
                request.update_env(user=request.session.uid)

        values = {k: v for k, v in request.params.items() if
                  k in SIGN_UP_REQUEST_PARAMS}

        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            try:
                if request.params.get('db'):
                    request.session.db = request.params.get('db')
                    request.update_env(user=None)

                credential = {key: value for key, value in
                              request.params.items() if
                              key in CREDENTIAL_PARAMS and value}
                credential.setdefault('type', 'password')

                if request.env['res.users']._should_captcha_login(credential):
                    request.env['ir.http']._verify_request_recaptcha_token(
                        'login')

                auth_info = request.session.authenticate(request.env,
                                                         credential)
                request.params['login_success'] = True
                return request.redirect(
                    self._login_redirect(auth_info['uid'], redirect=redirect))

            except odoo.exceptions.AccessDenied as e:
                # --- CORRECCIÓN DE ERROR EN MANTENIMIENTO ---
                if e.args == odoo.exceptions.AccessDenied().args:
                    error_msg = "Usuario o contraseña incorrectos"
                else:
                    error_msg = e.args[0]

                # Si el mantenimiento está activo, devolvemos TU template con el error
                if maintenance_record and maintenance_record.active_maintenance:
                    response = request.render(
                        'sicpro_modulo_web_login.sicpro_template_mantenimiento',
                        get_maintenance_values(error_msg))
                    response.headers['Cache-Control'] = 'no-cache'
                    return response

                values[
                    'error'] = error_msg  # --------------------------------------------
        else:
            if 'error' in request.params and request.params.get(
                'error') == 'access':
                values['error'] = 'Solo los empleados pueden acceder a esta base de datos.'

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        response = request.render(
            'sicpro_modulo_web_login.sicpro_template_final', values)
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response


class WebsiteSicpro(HomeSicpro):
    @http.route(website=True, auth="public", sitemap=False)
    def web_login(self, *args, **kw):
        return super(WebsiteSicpro, self).web_login(*args, **kw)