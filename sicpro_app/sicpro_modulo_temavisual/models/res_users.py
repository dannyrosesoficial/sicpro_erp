# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    chatter_position = fields.Selection(
        [("normal", "Abajo"), ("sided", "Derecha")],
        string="Posición Chat", required=True, default="sided",)

    def __init__(self, pool, cr):
        super(ResUsers, self).__init__(pool, cr)

        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(["chatter_position"])

        # type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        # type(self).SELF_READABLE_FIELDS.extend(["chatter_position"])