# -*- coding: utf-8 -*-

import json

from odoo import http
from odoo.http import request


class OnedriveAuth(http.Controller):

    @http.route('/onedrive/authentication', type='http', auth="public")
    def oauth2callback(self, **kw):
        state = json.loads(kw['state'])
        backup_config = request.env['sicpro.modulo.backup.server.local'].sudo().browse(state.get('backup_config_id'))
        backup_config.get_onedrive_tokens(kw.get('code'))
        url_return = state.get('url_return')
        return request.redirect(url_return)

    @http.route('/google_drive/authentication', type='http', auth="public")
    def gdrive_oauth2callback(self, **kw):
        state = json.loads(kw['state'])
        backup_config = request.env['sicpro.modulo.backup.server.local'].sudo().browse(state.get('backup_config_id'))
        backup_config.get_gdrive_tokens(kw.get('code'))
        url_return = state.get('url_return')
        return request.redirect(url_return)
