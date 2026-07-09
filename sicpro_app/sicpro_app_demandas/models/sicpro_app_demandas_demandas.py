# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _


class DemandasDemandas(models.Model):
    _name = "sicpro.app.demandas.demandas"
    _description = 'Document'
    _order = 'id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Nombre', required=True)
