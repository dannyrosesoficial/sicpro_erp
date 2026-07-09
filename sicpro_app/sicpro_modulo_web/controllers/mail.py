# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging
import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from werkzeug.urls import url_encode, iri_to_uri

from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request

# Danny: Importamos la clase Home original 🌹
from odoo.addons.web.controllers.home import Home

_logger = logging.getLogger(__name__)


# ----------------------------------------------------------
# Odoo Web helpers - Compatibilidad Odoo 19
# ----------------------------------------------------------

def get_db_monodb():
    try:
        return http.db_monodb(request.httprequest)
    except (AttributeError, Exception):
        try:
            return http.root.db_monodb(request.httprequest)
        except:
            return None


def _get_login_redirect_url(uid, redirect=None):
    if request.session.uid:
        return redirect or '/odoo'

    user = request.env['res.users'].sudo().browse(uid)
    url = user._mfa_url() if hasattr(user, '_mfa_url') else '/odoo/login'

    if not redirect:
        return url

    parsed = werkzeug.urls.url_parse(url)
    qs = parsed.decode_query()
    qs['redirect'] = redirect
    return parsed.replace(query=werkzeug.urls.url_encode(qs)).to_url()


def abort_and_redirect(url):
    r = request.httprequest
    response = werkzeug.utils.redirect(url, 302)
    response = r.app.get_response(r, response, explicit_session=False)
    werkzeug.exceptions.abort(response)


def ensure_db(redirect='/odoo/database/selector'):
    db = request.params.get('db') and request.params.get('db').strip()
    if db and db not in http.db_filter([db]):
        db = None
    if db and not request.session.db:
        r = request.httprequest
        url_redirect = werkzeug.urls.url_parse(r.base_url)
        if r.query_string:
            query_string = iri_to_uri(r.query_string)
            url_redirect = url_redirect.replace(query=query_string)
        request.session.db = db
        abort_and_redirect(url_redirect)
    if not db and request.session.db and http.db_filter([request.session.db]):
        db = request.session.db
    if not db:
        db = get_db_monodb()
    if not db:
        werkzeug.exceptions.abort(werkzeug.utils.redirect(redirect, 303))
    if db != request.session.db:
        request.session.logout()
    request.session.db = db


# ----------------------------------------------------------
# Odoo Web web Controllers - SICPRO 🌹
# ----------------------------------------------------------

class SicproHome(Home):

    @http.route('/odoo/inicio/', auth="public", website=True, sitemap=False)
    def web_inicio(self, **kwargs):
        return request.render("sicpro_modulo_web.web_plantilla_inicio", {})

    @http.route(['/', '/web', '/odoo'], type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        # Danny: Log para confirmar que la versión nueva de SICPRO está cargada 🌹
        _logger.info(">>> Cargando Web Client SICPRO Odoo 19")

        ensure_db()

        if not request.session.uid:
            return request.redirect('/odoo/inicio', 303)

        if kw.get('redirect'):
            return request.redirect(kw.get('redirect'), 303)

        # Danny: ELIMINADO request.uid = ... para evitar NotImplementedError 🌹
        # Usamos la nueva API de Odoo 19:
        request.update_env(user=request.session.uid)

        try:
            context = request.env['ir.http'].webclient_rendering_context()
            response = request.render('web.webclient_bootstrap',
                                      qcontext=context)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
        except AccessError:
            return request.redirect('/odoo/inicio?error=access')

    def _login_redirect(self, uid, redirect=None):
        return _get_login_redirect_url(uid, redirect)