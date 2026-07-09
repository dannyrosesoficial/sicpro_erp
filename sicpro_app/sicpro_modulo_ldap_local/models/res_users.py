# -*- coding: utf-8 -*-

import logging

# import sicpro_modulo_ldap_query
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = 'res.users'

    tipo_usuario = fields.Selection([('ldap', 'LDAP'), ('local', 'Local'), ], default='ldap', string='Tipo de Usuario')
    pep = fields.Char(string='No. Plaza', required=False)
    buscar_pep = fields.Many2one(comodel_name='sicpro.app.modulo.ldap.registros', string='Buscar No. PEP',
                                 required=False)

    @api.onchange('buscar_pep')
    def buscar_usuario_ldap(self):
        if self.buscar_pep:
            self.sudo().name = self.buscar_pep.cn
            self.sudo().login = self.buscar_pep.uid
            self.sudo().email = self.buscar_pep.mail
            self.pep = self.buscar_pep.employeeNumber
            self.buscar_pep = None
