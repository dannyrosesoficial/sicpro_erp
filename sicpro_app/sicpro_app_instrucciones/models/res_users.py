# -*- coding: utf-8 -*-


from odoo import fields, models


class UsersContext(models.Model):
    _inherit = 'res.users'

    intrucciones_context = fields.Boolean(required=False, default=False)
