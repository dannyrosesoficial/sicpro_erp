# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import odoo
from odoo.http import request, Session
from odoo.modules.registry import Registry


def authenticate_without_password(self, dbname, login, env):
    if not all([dbname, login]):
        return None

    user_domain = [("login", "=", login)]
    user = env['res.users'].search(user_domain, limit=1)
    if not user:
        return None
    # Store session data
    self.update({'uid': None, 'pre_login': login, 'pre_uid': user.id})

    if not user._mfa_url():
        with Registry(dbname).cursor() as cr:
            user_env = odoo.api.Environment(cr, user.id, {})
            self.finalize(user_env)

    request = odoo.http.request
    if request and getattr(request, 'session', None) is self and getattr(
        request, 'db', None) == dbname:
        request.env = odoo.api.Environment(request.env.cr, self.uid,
                                           self.context)
        request.update_context(**self.context)
    return user.id


Session.authenticate_without_password = authenticate_without_password
