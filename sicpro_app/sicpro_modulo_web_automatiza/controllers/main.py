# -*- coding: utf-8 -*-


from odoo import http
from odoo.http import request


class WebAutomatiza(http.Controller):

    @http.route('/web/automatiza/', auth="public", website=True)
    def web_automatiza_correos(self, **kwargs):
        return request.render("sicpro_modulo_web_automatiza.web_automatiza_correos", {})
