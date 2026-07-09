# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import http
from odoo.http import request, route


class MenuMarcadores(http.Controller):

    @route('/web/sicpro_menu_marcadores/data', methods=['POST'],
           type='jsonrpc', auth='user')
    def menu_bookmark_data(self, **kwargs):
        return request.env['sicpro.menu.marcadores'].search_read(
            [('user_id', '=', request.session.uid)], [])

    @route('/web/sicpro_menu_marcadores/add', methods=['POST'], type='jsonrpc',
           auth='user')
    def menu_bookmark_add(self, **kwargs):
        new_bookmark = {'name': kwargs.get('name'), 'url': kwargs.get('url'),
            'user_id': request.session.uid, }
        return request.env['sicpro.menu.marcadores'].create(new_bookmark).id
