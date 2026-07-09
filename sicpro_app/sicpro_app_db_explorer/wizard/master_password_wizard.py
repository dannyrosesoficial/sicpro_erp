# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class SicproMasterPasswordWizard(models.TransientModel):
    _name = 'sicpro.app.db.master.password.wizard'
    _description = 'Confirmación de Contraseña Maestra'

    table_id = fields.Many2one('sicpro.app.db.explorer.table')
    password_input = fields.Char(string="Contraseña de Seguridad", required=True)

    def action_confirm(self):
        master_pwd = self.env['ir.config_parameter'].sudo().get_param('sicpro.app.db.explorer.master_password')
        if self.password_input == master_pwd:
            self.table_id.write({'state': 'unlocked'})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Seguridad'),
                    'message': _('Modo edición desbloqueado para esta tabla.'),
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            raise AccessError(_("Contraseña incorrecta. Intento registrado en auditoría de seguridad."))