# -*- coding: utf-8 -*-

from odoo import fields, models


class DesactivarUsersRoles(models.Model):
    _inherit = "sicpro.modulo.roles"

    tipo_desactivar = fields.Selection(
        string='Tipo Desactivación',
        selection=[('ldap', 'Desactivar por LDAP'), ('registro', 'Desactivar por Registro'),
                   ('acceso', 'Desactivar por Acceso'), ], required=False,
        help='Solo se debe seleccionar para los roles que se configuran en la desactivación por: '
             'No existir en el LDAP empresarial, por no validar el registro de acceso o por no entrar al sistema en '
             'el periodo establecido')
