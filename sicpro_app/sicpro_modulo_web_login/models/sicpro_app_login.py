# -*- coding: utf-8 -*-

from odoo import models, fields


class SicproConfigLoginVersion(models.Model):
    _name = 'sicpro.app.login.config.version'
    _description = 'Configuración de la Version de la Aplicación'

    name = fields.Char(string='Versión', required=True)
    config = fields.Char(required=True, default='config_version', readonly=True)

    _sql_constraints = [('name_company_uniq', 'unique(config)', 'Ya existe la configuración de la versión'), ]
