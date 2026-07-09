# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AutoDatabaseUrlGitlab(models.Model):
    _name = 'sicpro.modulo.backup.server.gitlab'
    _description = 'Url GitLab donde se sincroniza los backups'

    name = fields.Char(string='URL GitLab', required=True)
    active = fields.Boolean(string='Archivado', default=True)

    @api.constrains('active')
    def _check_url_gitlab_unico(self):
        uniq = self.env['sicpro.modulo.backup.server.gitlab'].search(
            ['&', ("active", "=", True), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡Ya se encuentra configurada un url de GitLab en el sistema!. "
                                    "Si cree que es un error contacte al administrador"))
