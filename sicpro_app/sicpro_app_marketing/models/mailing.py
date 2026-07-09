# -*- coding: utf-8 -*-


from odoo import fields, models


class MassMailing(models.Model):
    _inherit = 'mailing.mailing'

    def _compute_email_from_reply_to(self):
        user = self.env['res.users'].search([('active', '=', False), ('id', '=', 1)]).email_formatted
        return user

    email_from = fields.Char(string='Enviado desde', required=True, store=True, readonly=False,
                             default=_compute_email_from_reply_to)
    reply_to = fields.Char(string='Responder A', readonly=False, store=True, default=_compute_email_from_reply_to,
                           help='Dirección de respuesta')
