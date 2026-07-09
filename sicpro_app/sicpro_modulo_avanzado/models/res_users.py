# -*- coding: utf-8 -*-

import logging

import pytz
from odoo import SUPERUSER_ID, api, models
from odoo.exceptions import AccessDenied
from odoo.http import request

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def check_user_group_admin(self, user_id):
        if user_id in self.env.ref("base.group_system").users.ids:
            return True
        else:
            return False
