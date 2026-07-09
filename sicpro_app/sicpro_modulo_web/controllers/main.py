# -*- encoding: utf-8 -*-

import logging

from odoo import http
from odoo.addons.web.controllers.home import Home, ensure_db
from odoo.http import request

_logger = logging.getLogger(__name__)


class SicproHome(Home):

    # 1. Tu página de inicio personalizada
    @http.route('/odoo/inicio/', auth="public", website=True, sitemap=False)
    def web_inicio(self, **kwargs):
        ensure_db()
        return request.render("sicpro_modulo_web.web_plantilla_inicio", {})

    # 2. El controlador principal que intercepta la entrada
    @http.route(['/web', '/sicpro', '/odoo', '/odoo/<path:subpath>',
                 '/scoped_app/<path:subpath>', '/'], type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        # 1. Aseguramos la base de datos
        ensure_db()

        # Si no hay usuario y es una petición de navegación (GET)
        # en lugar de mandar a '/web/login', mandamos a tu nueva página
        if not request.session.uid and request.httprequest.method == 'GET':
            return request.redirect('/odoo/inicio', 303)

        # Si el usuario ya está logueado o es una petición de datos (POST/RPC),
        # llamamos al método original (super) para que Odoo funcione con normalidad
        # y no dé errores 404 al guardar registros.
        return super(SicproHome, self).web_client(s_action=s_action, **kw)

    # # 3. Mantenemos el redireccionamiento de login alineado con /odoo
    def _login_redirect(self, uid, redirect=None):
        if not redirect:
            redirect = '/odoo'
        return super()._login_redirect(uid, redirect=redirect)
