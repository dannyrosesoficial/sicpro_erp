# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class SicproWebRoles(models.Model):
    _name = 'sicpro.modulo.web.registro.roles'
    _description = 'Roles para el registro de usuarios'
    _order = "sequence, id"

    name = fields.Char(string='Nombre', required=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    active = fields.Boolean(string='Archivado', default=True, index=True)
    automatizar_usuario_externo = fields.Boolean(string="Usuario Externo",
                                                 required=False,
                                                 default="False",
                                                 help='Asigna automáticamente los roles seleccionados al registro de usuario externo del sistema,')
    descripcion = fields.Char(string='Descripción', required=True)
    roles = fields.Many2many('res.users.role', 'web_registro_roles_acceso_rel',
                             string='Roles', required=True)
