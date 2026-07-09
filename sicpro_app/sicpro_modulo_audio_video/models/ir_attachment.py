# -*- coding: utf-8 -*-


from odoo import models, fields


class GrabacionAttachment(models.Model):
    _inherit = 'ir.attachment'

    tipo_grabacion = fields.Selection(string='Tipo_grabacion',
                                      selection=[('audio', 'audio'),
                                                 ('video', 'video'), ],
                                      required=False, )
