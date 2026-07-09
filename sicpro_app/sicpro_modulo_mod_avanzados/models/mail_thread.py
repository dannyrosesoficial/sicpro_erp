# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import api, fields, models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def message_subscribe(self, partner_ids=None, channel_ids=None, subtype_ids=None):
        ir_config = self.env['ir.config_parameter']
        app_stop_subscribe = True if ir_config.get_param('app_stop_subscribe', False) == "True" else False
        if app_stop_subscribe:
            return True
        else:
            return super(MailThread, self).message_subscribe(partner_ids, subtype_ids)

    def _message_subscribe(self, partner_ids=None, channel_ids=None, subtype_ids=None, customer_ids=None):
        ir_config = self.env['ir.config_parameter']
        app_stop_subscribe = True if ir_config.get_param('app_stop_subscribe', False) == "True" else False
        if app_stop_subscribe:
            return True
        else:
            return super(MailThread, self)._message_subscribe(partner_ids, subtype_ids, customer_ids)

    def _message_auto_subscribe_followers(self, updated_values, default_subtype_ids):
        ir_config = self.env['ir.config_parameter']
        app_stop_subscribe = True if ir_config.get_param('app_stop_subscribe', False) == "True" else False
        if app_stop_subscribe:
            return []
        else:
            return super(MailThread, self)._message_auto_subscribe_followers(updated_values, default_subtype_ids)

    def _message_auto_subscribe_notify(self, partner_ids, template):
        ir_config = self.env['ir.config_parameter']
        app_stop_subscribe = True if ir_config.get_param('app_stop_subscribe', False) == "True" else False
        if app_stop_subscribe:
            return True
        else:
            return super(MailThread, self)._message_auto_subscribe_notify(partner_ids, template)
