# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes
#    Copyright (C) 2024-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import os
from markupsafe import Markup
from odoo import http
from odoo.http import request
from odoo.modules import get_module_resource


class SicproCatalogoController(http.Controller):

    @http.route('/modulos', type='http', auth='public', website=True)
    def listado_modulos(self, **kwargs):
        """ Filtra y muestra los módulos instalados cuyo autor sea Daniel Barrero o SICPRO ERP """
        modulos = request.env['ir.module.module'].sudo().search(
            [('state', '=', 'installed'), '|',
                ('author', 'ilike', 'Daniel Barrero'),
                ('author', 'ilike', 'SICPRO ERP')], order='shortdesc asc')

        return request.render(
            'sicpro_modulo_web_catalogo.catalogo_modulos_page',
            {'modulos': modulos})

    @http.route('/modulos/<string:module_name>', type='http', auth='public',
                website=True)
    def detalle_modulo(self, module_name, **kwargs):
        """ Renderiza de forma segura el index.html de la carpeta static/description """
        modulo = request.env['ir.module.module'].sudo().search(
            [('name', '=', module_name), ('state', '=', 'installed'), '|',
                ('author', 'ilike', 'Daniel Barrero'),
                ('author', 'ilike', 'SICPRO ERP')], limit=1)

        if not modulo:
            return request.not_found()

        # Localizamos físicamente la ruta del archivo index.html en el servidor
        html_content = ""
        path = get_module_resource(module_name, 'static', 'description',
                                   'index.html')

        if path and os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        else:
            # Plantilla de contingencia elegante si el módulo no posee index.html todavía
            html_content = f"""
            <div class="text-center py-5 my-5" style="font-family: sans-serif;">
                <div class="display-1 text-muted mb-4">📦</div>
                <h2 class="fw-bold text-secondary">{modulo.shortdesc}</h2>
                <p class="lead text-muted max-w-md mx-auto">Este módulo se encuentra operando activamente en el Core pero no cuenta con una ficha descriptiva pública en su directorio estático.</p>
            </div>
            """

        return request.render('sicpro_modulo_web_catalogo.detalle_modulo_page',
                              {'modulo': modulo,
                                  'html_content': Markup(html_content)
                                  # Encapsulado Markup seguro para renderizar HTML nativo
                              })