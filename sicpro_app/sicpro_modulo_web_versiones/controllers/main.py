# -*- coding: utf-8 -*-


from odoo import http
from odoo.http import request


class WebVersiones(http.Controller):

    @http.route('/web/versiones/', auth="public", website=True)
    def plantilla_web_versiones(self, **kwargs):
        return request.render("sicpro_modulo_web_versiones.web_plantilla_versiones", {})
