# -*- coding: utf-8 -*-


from odoo import models
from odoo.addons.sicpro_modulo_base_correos_entrantes.models.fetchmail import FetchmailServer


class SoporteTicket(models.Model):
    _inherit = 'sicpro.app.soporte'

    # solícito que se revisen la existencia de correos electrónicos de solicitudes de usuario
    def solicitar_correos_soporte(self):
        # llamo al método heredado del módulo base_correos_entrantes
        MailFetchmail = self.env['fetchmail.server'].search([('active', '=', True)])
        for mail in MailFetchmail:
            FetchmailServer.fetch_mail(mail)
