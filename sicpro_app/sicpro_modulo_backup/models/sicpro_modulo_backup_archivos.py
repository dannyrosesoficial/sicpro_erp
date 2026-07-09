# -*- coding: utf-8 -*-

from odoo import models, fields


class DbBackupArchivos(models.Model):
    _name = 'sicpro.modulo.backup.archivos'
    _description = 'Registro de archivos de las salvas automáticas del sistema'

    name = fields.Char('archivo', required=False)
    active_local = fields.Boolean('active local', default=True)
    active_webdav = fields.Boolean('active models', default=True)
    active_sftp = fields.Boolean('active sftp', default=True)
    fecha_subida = fields.Date(string="fecha_subida",
                               default=lambda self: fields.Date.context_today(self))
