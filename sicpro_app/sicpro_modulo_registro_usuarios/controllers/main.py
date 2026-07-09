# -*- coding: utf-8 -*-

from odoo.addons.web.controllers import main
from odoo.http import request
from odoo.exceptions import Warning
import odoo
import odoo.modules.registry
from odoo.tools.translate import _
from odoo import http


class Home(main.Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        main.ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

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
                user_rec = request.env['res.users'].sudo().search(
                    [('login', '=', request.params['login'])])
                # verifica que el usuario tenga alguna dirección
                # ip en la lista de filtros
                if user_rec.registro_ips:
                    ip_list = []
                    for rec in user_rec.registro_ips:
                        ip_list.append(rec.ip_address)
                    # evalúa que la dirección ip asignada
                    # sea la que se esta usando
                    if ip_address in ip_list:
                        try:
                            uid = request.session.authenticate(
                                request.session.db, request.params['login'],
                                request.params['password'])
                            request.params['login_success'] = True
                            return http.redirect_with_hash(
                                self._login_redirect(uid, redirect=redirect))
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
                                uid = request.session.authenticate(
                                    request.session.db,
                                    request.params['login'],
                                    request.params['password'])
                                request.params['login_success'] = True
                                return http.redirect_with_hash(
                                    self._login_redirect(uid,
                                                         redirect=redirect))
                            except odoo.exceptions.AccessDenied as e:
                                request.uid = old_uid
                                if e.args == odoo.exceptions.AccessDenied().args:
                                    values['error'] = _(
                                        "Usuario/Contraseña incorrecta")
                                else:
                                    values['error'] = e.args[0]
                        else:
                            request.uid = old_uid
                            values['error'] = _("Error en el Acceso Local o VPN")
                # Acción si no tiene direcciones ip, lo que significa que
                # puede acceder sin filtros
                else:
                    try:
                        uid = request.session.authenticate(request.session.db,
                                                           request.params[
                                                               'login'],
                                                           request.params[
                                                               'password'])
                        request.params['login_success'] = True
                        return http.redirect_with_hash(
                            self._login_redirect(uid, redirect=redirect))
                    except odoo.exceptions.AccessDenied as e:
                        request.uid = old_uid
                        if e.args == odoo.exceptions.AccessDenied().args:
                            values['error'] = _(
                                "Usuario/Contraseña incorrecta.")
        response = request.render('web.login', values)
        return response
