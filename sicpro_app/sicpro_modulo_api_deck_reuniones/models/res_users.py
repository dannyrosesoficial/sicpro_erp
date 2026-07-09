# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, Command
from odoo.addons.google_calendar.utils.google_calendar import \
    GoogleCalendarService, InvalidSyncToken
from odoo.addons.google_calendar.models.google_sync import \
    google_calendar_token
from odoo.loglevels import exception_to_unicode


class User(models.Model):
    _inherit = 'res.users'

    caldav_calendario_activo = fields.Boolean(string='Activar Sync')
