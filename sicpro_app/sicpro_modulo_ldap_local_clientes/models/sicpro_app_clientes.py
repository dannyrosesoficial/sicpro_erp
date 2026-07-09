# -*- coding: utf-8 -*-

import logging

# import sicpro_modulo_ldap_query
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AppClientes(models.Model):
    _inherit = 'sicpro.app.clientes'

    tipo_cliente = fields.Selection([('ldap', 'LDAP'), ('local', 'Local'), ], default='ldap', string='Tipo de Cliente')
    pep = fields.Char(string='No. Plaza', required=False)
    buscar_pep = fields.Many2one(comodel_name='sicpro.app.modulo.ldap.registros', string='Buscar No. PEP',
                                 required=False)

    @api.onchange('buscar_pep')
    def buscar_usuario_ldap(self):
        if self.buscar_pep:
            self.sudo().name = self.buscar_pep.cn
            self.sudo().cargo = self.buscar_pep.title
            self.sudo().telefono_fijo = self.buscar_pep.telephoneNumber
            self.sudo().telefono_movil = self.buscar_pep.mobile
            self.sudo().correo = self.buscar_pep.mail
            self.pep = self.buscar_pep.employeeNumber
            uo = self.env['sicpro.nomenclador.territorios'].sudo().search([('abreviatura', '=', self.buscar_pep.ou)]).id
            territorio = self.env['sicpro.app.clientes'].sudo().search(
                ['&', ('tipo_registro', '=', 'entidad'), ('territorio', '=', uo)]).id
            if territorio:
                self.entidad = territorio
            self.buscar_pep = None


