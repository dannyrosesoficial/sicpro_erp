# -*- coding: utf-8 -*-


from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    marketing_contacto = fields.Many2one(comodel_name='mailing.contact', string='Contacto Marketing')

