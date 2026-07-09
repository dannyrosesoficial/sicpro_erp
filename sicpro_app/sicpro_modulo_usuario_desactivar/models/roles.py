# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class DesactivarUsersRoles(models.Model):
    _inherit = "res.users.role"

    tipo_desactivar = fields.Selection(string='Tipo Desactivación',
        selection=[('ldap', 'Desactivar por LDAP'),
                   ('registro', 'Desactivar por Registro'),
                   ('acceso', 'Desactivar por Acceso'), ], required=False,
        help='Solo se debe seleccionar para los roles que se configuran en la desactivación por: '
             'No existir en el LDAP empresarial, por no validar el registro de acceso o por no entrar al sistema en '
             'el periodo establecido')
