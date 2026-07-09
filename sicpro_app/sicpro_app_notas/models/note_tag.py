# -*- coding: utf-8 -*-


from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class Stage(models.Model):
    _inherit = "note.tag"

    color = fields.Integer(string='Color', default=lambda self: _default_color())


