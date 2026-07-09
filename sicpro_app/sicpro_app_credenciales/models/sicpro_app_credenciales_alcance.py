# -*- coding: utf-8 -*-

import base64
from datetime import timedelta,date,datetime
from odoo.modules.module import get_module_resource
from odoo import api, fields, models, _
from pytz import timezone, UTC
from odoo.tools import format_time
from random import randint


class CredencialesAccesos(models.Model):
    _name = 'sicpro.app.credenciales.alcance'
    _description = "Tipo de Credenciales"
    _order = 'name'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Nombre", required="True")
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())