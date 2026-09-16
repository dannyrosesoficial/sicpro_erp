# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home


SICPRO_URL_PREFIX = '/sicpro'
ODOO_URL_PREFIX = '/odoo'


def _odoo_to_sicpro(url):
    """Convert an Odoo web-client URL to the SICPRO canonical URL."""
    if not url:
        return url

    if url == ODOO_URL_PREFIX:
        return SICPRO_URL_PREFIX

    if url.startswith(f'{ODOO_URL_PREFIX}/'):
        return f'{SICPRO_URL_PREFIX}{url[len(ODOO_URL_PREFIX):]}'

    return url


class SicproHome(Home):
    """Expose the Odoo web client through the /sicpro URL prefix."""

    @http.route(
        ['/sicpro', '/sicpro/<path:subpath>'],
        type='http',
        auth='none',
        readonly=True,
    )
    def sicpro_web_client(self, s_action=None, **kw):
        return super().web_client(s_action=s_action, **kw)

    def _login_redirect(self, uid, redirect=None):
        """Keep Odoo's login logic and only change the web-client prefix."""
        url = super()._login_redirect(uid, redirect=redirect)
        return _odoo_to_sicpro(url)

    @http.route('/', type='http', auth='none')
    def index(self, s_action=None, db=None, **kw):
        """Keep Odoo's root behavior, canonicalizing only /odoo redirects."""
        response = super().index(s_action=s_action, db=db, **kw)

        if (
            request.db
            and request.session.uid
            and response.status_code in (301, 302, 303, 307, 308)
        ):
            location = response.headers.get('Location')
            new_location = _odoo_to_sicpro(location)

            if new_location != location:
                response.headers['Location'] = new_location

        return response
