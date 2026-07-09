# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, modules, fields


class Partner(models.Model):
    _inherit = ['res.partner']

    area = fields.Char(string='Área', required=False)
