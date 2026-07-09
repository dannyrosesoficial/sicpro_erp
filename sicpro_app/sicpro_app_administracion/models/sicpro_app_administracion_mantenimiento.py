# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SicproMantenimiento(models.Model):
    _name = 'sicpro.app.administracion.mantenimiento'
    _description = 'Aplicación para la administración de SICPRO ERP'

    name = fields.Char(string='Mantenimiento',
                                default='MODO MANTENIMIENTO')
    activar_mantenimiento = fields.Boolean(string='Activar Login Mantenimiento',
                                           required=False)

    @api.onchange('activar_mantenimiento')
    def onchange_activar_mantenimiento(self):
        data1 = self.env['ir.attachment'].search([('id_img_login', '=', 1)])
        data2 = self.env['ir.attachment'].search([('id_img_login', '=', 2)])
        if self.activar_mantenimiento:
            for item in data1:
                item.use_as_background = 0
            for item in data2:
                item.use_as_background = 1
        else:
            for item in data1:
                item.use_as_background = 1
            for item in data2:
                item.use_as_background = 0

    def mod_desintalar_ldaps(self):
        # desinstalar los modulos LDAPS
        modulo_ldap = self.env['ir.module.module'].search([('name', '=', 'auth_ldap')])
        modulo_ldap.button_immediate_uninstall()

    def mod_instalar_ldaps(self):
        # instalar los modulos LDAPS
        modulo_ldap = self.env['ir.module.module'].search(
            [('name', '=', 'sicpro_modulo_ldaps')])
        modulo_ldap.button_immediate_install()










