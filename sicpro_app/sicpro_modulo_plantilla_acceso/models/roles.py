# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsersRoles(models.Model):
    _inherit = "sicpro.modulo.roles"

    clave_solicitud = fields.Char(string="*Código del ROL*", required=True)
