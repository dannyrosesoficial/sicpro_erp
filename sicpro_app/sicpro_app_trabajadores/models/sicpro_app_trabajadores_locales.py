# -*- coding: utf-8 -*-

from odoo import api, fields, models


class TrabajadoresLocales(models.Model):
    _name = 'sicpro.app.trabajadores.local'
    _description = 'Locales del trabajador'

    name = fields.Char(string="Local", required=False, )
    locales_id = fields.Char(required=False, )
