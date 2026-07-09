# -*- coding: utf-8 -*-


from odoo import http
from odoo.http import request


class WebPlugins(http.Controller):

    @http.route('/web/plugins/', auth="public", website=True)
    def web_descarga_plugins(self, **kwargs):
        return request.render("sicpro_modulo_web_plugins.web_plugins", {})
