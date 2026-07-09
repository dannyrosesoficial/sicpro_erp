# -*- coding: utf-8 -*-

from odoo import fields, models


class Uom(models.Model):
    _inherit = 'uom.uom'

    timesheet_widget = fields.Char("Widget",
                                   help="Widget usado en el webclient.")
