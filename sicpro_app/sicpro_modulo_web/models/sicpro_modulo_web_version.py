# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SicproWebVersion(models.Model):
    _name = 'sicpro.modulo.web.version'
    _description = 'Configuración de la Version del Sistema'

    name = fields.Char(string='Versión', required=True)
    active = fields.Boolean(string='Archivado', default=True)

    @api.constrains('active')
    def _check_vesion_unico(self):
        uniq = self.env['sicpro.modulo.web.version'].search(['&', ("active", "=", True), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡Ya se encuentra configurada la versión del sistema!. "
                                    "Si cree que es un error contacte al administrador"))
