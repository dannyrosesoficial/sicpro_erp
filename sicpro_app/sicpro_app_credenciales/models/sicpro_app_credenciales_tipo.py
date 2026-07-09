# -*- coding: utf-8 -*-

import base64
from datetime import timedelta, date, datetime
from odoo.modules.module import get_module_resource
from odoo import api, fields, models, _
from pytz import timezone, UTC
from odoo.tools import format_time
from random import randint


def _default_color():
    return randint(1, 11)


class CredencialesTipo(models.Model):
    _name = 'sicpro.app.credenciales.tipo'
    _description = "Tipo de Credenciales"
    _order = 'name'

    name = fields.Char(string="Tipo", required="True")
    personal_externo = fields.Boolean(string='Personal Externo', required=False)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
