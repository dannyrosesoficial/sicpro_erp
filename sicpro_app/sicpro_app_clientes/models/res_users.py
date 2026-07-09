# -*- coding: utf-8 -*-


from odoo import fields, models


class Users(models.Model):

    _inherit = 'res.users'

    user_inversionista = fields.Boolean("¿Es inversionista?")
