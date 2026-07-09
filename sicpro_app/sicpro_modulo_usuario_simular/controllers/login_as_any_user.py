# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import http
from odoo.http import request


class UserSwitch(http.Controller):

    @http.route('/switch/user', type='jsonrpc', auth='user')
    def user_switch(self):
        return request.env.user._is_admin()

    @http.route('/switch/admin', type='jsonrpc', auth='user')
    def switch_admin(self):
        session = request.session
        pre_uid = session.get('previous_user')
        pre_user = request.env['res.users'].browse(pre_uid)
        if pre_user and pre_user._is_admin():
            session.authenticate_without_password(request.env.cr.dbname,
                                                  pre_user.login, request.env)
            return {'type': 'ir.actions.act_url', 'url': '/', 'target': 'self'}
        return True
