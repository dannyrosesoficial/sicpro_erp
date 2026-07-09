# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SicproAdministracion(models.Model):
    _name = 'sicpro.app.administracion'
    _description = 'Aplicación para la administración de SICPRO ERP'

    name = fields.Char(string='Admin', default='ADMINISTRACIÓN')



