# -*- encoding: utf-8 -*-

import logging

import odoo
import odoo.modules.registry
from odoo import http
# Importo herencia del controller de sicpro.modulo.web.login
from odoo.addons.sicpro_modulo_web_login.controllers.main import HomeLogin
from odoo.addons.sicpro_modulo_web_login.controllers.main import ensure_db
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

# ----------------------------------------------------------
# sicpro_modulo_web web Controllers
# ----------------------------------------------------------


class HomeHerencia(HomeLogin):

    # *************** IMPORTANTE ***************
    # Heredo
    # si se realizan cambios en este método se debe replicar en el código del controller del login
    @http.route('/web/mtto2db/', type='http', auth="none")
    def web_modo_mantenimiento(self, redirect=None, **kw):
        # si está en mantenimiento redirecciono al login de entrada
        ensure_db()

        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            # creo la dirección ip
            ip_address = request.httprequest.environ['REMOTE_ADDR']
            # creo la dirección vpn
            vpn_address = ip_address[:3] + '.*'

            if request.params['login']:
                user_rec = request.env['res.users'].sudo().search([('login', '=', request.params['login'])])
                # verífica que el usuario tenga alguna dirección ip en la lista de filtros
                if user_rec.registro_ips:
                    ip_list = []
                    for rec in user_rec.registro_ips:
                        ip_list.append(rec.ip_address)
                    # evalúa que la dirección ip asignada sea la que se está usando
                    if ip_address in ip_list:
                        try:
                            uid = request.session.authenticate(request.session.db, request.params['login'],
                                                               request.params['password'])
                            request.params['login_success'] = True
                            return request.redirect(self._login_redirect(uid, redirect=redirect))
                        except odoo.exceptions.AccessDenied as e:
                            request.uid = old_uid
                            if e.args == odoo.exceptions.AccessDenied().args:
                                values['error'] = _("Usuario/Contraseña incorrecta")
                            else:
                                values['error'] = e.args[0]
                    else:
                        # verifico las direcciones vpn
                        if vpn_address in ip_list:
                            try:
                                uid = request.session.authenticate(request.session.db, request.params['login'],
                                                                   request.params['password'])
                                request.params['login_success'] = True
                                return request.redirect(self._login_redirect(uid, redirect=redirect))
                            except odoo.exceptions.AccessDenied as e:
                                request.uid = old_uid
                                if e.args == odoo.exceptions.AccessDenied().args:
                                    values['error'] = _("Usuario/Contraseña incorrecta")
                                else:
                                    values['error'] = e.args[0]
                        else:
                            request.uid = old_uid
                            values['error'] = _("Error en el Acceso Local o VPN")
                # Acción si no tiene direcciones ip, lo que significa que puede acceder sin filtros
                else:
                    try:
                        uid = request.session.authenticate(request.session.db, request.params['login'],
                                                           request.params['password'])
                        request.params['login_success'] = True
                        return request.redirect(self._login_redirect(uid, redirect=redirect))
                    except odoo.exceptions.AccessDenied as e:
                        request.uid = old_uid
                        if e.args == odoo.exceptions.AccessDenied().args:
                            values['error'] = _("Usuario/Contraseña incorrecta")
                        else:
                            values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Solo tienen acceso los trabajadores con usuario en el sistema. '
                                    'Por favor contacte al administrador.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        response = request.render('sicpro_modulo_web_login.login_template', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    # Heredo
    def web_tipo_plantilla(self):
        plantilla_mtto = "sicpro_modulo_web_mantenimiento.web_plantilla_mantenimiento"
        plantilla_login = 'sicpro_modulo_web_login.login_template'

        # verífico que el sistema esté en mantenimiento
        mtto = request.env['sicpro.modulo.web.mantenimiento'].sudo().search([("active", "=", True)])
        # si está en mantenimiento redirecciono al la pagina de espera
        if mtto.activar_mantenimiento:
            plantilla = plantilla_mtto
        else:
            plantilla = plantilla_login
        return plantilla


