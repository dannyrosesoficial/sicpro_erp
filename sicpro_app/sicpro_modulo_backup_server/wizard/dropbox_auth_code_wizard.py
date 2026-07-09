# -*- coding: utf-8 -*-


from odoo import models, fields, api


class BackupServerDropboxAuth(models.TransientModel):
    _name = 'sicpro.modulo.backup.dropbox.auth'
    _description = 'Asistente de autenticación de Dropbox'

    dropbox_authorization_code = fields.Char(string='Código de Autorización')
    dropbox_auth_url = fields.Char(string='URL de autenticación de Dropbox', compute='_compute_dropbox_auth_url')

    @api.depends('dropbox_authorization_code')
    def _compute_dropbox_auth_url(self):
        backup_config = self.env['sicpro.modulo.backup.server.local'].browse(self.env.context.get('active_id'))
        dropbox_auth_url = backup_config.get_dropbox_auth_url()
        for rec in self:
            rec.dropbox_auth_url = dropbox_auth_url

    def action_setup_dropbox_token(self):
        backup_config = self.env['sicpro.modulo.backup.server.local'].browse(self.env.context.get('active_id'))
        backup_config.set_dropbox_refresh_token(self.dropbox_authorization_code)
