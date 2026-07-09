# -*- coding: utf-8 -*-
from odoo import models, fields


class SicproAdministracion(models.Model):
    _name = 'sicpro.app.administracion'
    _description = 'Aplicación para la administración de SICPRO ERP'

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string='Admin', default='ADMINISTRACIÓN')
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')


