# Copyright 2018, 2021 Heliconia Solutions Pvt Ltd (https://heliconia.io)

from odoo import fields, models


class PassUserBackup(models.TransientModel):
    """ Wizard que muestra el passuserbackup """
    _name = "pass.user.backup"
    _description = "Modelo para visualizar el PassUserBackup"

    def _default_pass_user_backup(self):
        backup = ''
        pass_user_backup = self._context.get('active_model') == 'res.users' and self._context.get('active_ids') or []
        for item in self.env['res.users'].browse(pass_user_backup):
            backup = item.pass_backup
        return backup

    pass_user_backup = fields.Char(string='PASSUSERBACKUP', default=_default_pass_user_backup)
