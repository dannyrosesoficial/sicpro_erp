# -*- coding: utf-8 -*-

from odoo import models
from odoo.http import request


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        user = request.env.user
        res = super(Http, self).session_info()
        if self.env.user.has_group('base.group_user'):
            res['api_rest_key'] = user.api_rest_key
        return res
