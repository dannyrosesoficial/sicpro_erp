# -*- coding: utf-8 -*-


from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class Stage(models.Model):
    _inherit = "note.stage"

    tableros_id = fields.Many2one('note.tableros', string='Tableros', required=True)


