# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsersWebRoles(models.Model):
    _inherit = "sicpro.modulo.roles"

    automatizar_usuario_externo = fields.Boolean(
        string="Usuario Externo", required=False, default="False",
        help='Asigna automáticamente los roles seleccionados al registro de usuario externo del sistema,')
    nombre_registro = fields.Char(string='Nombre de registro', compute='_compute_nombre_rol', )

    # género el nombre del rol que aparecerá en el registro del usuario
    def _compute_nombre_rol(self):
        for item in self:
            caracteres = len(item.name)
            indice = item.name.find(':')
            indice_inicial = indice + 2
            indice_final = indice_inicial + (caracteres - indice_inicial)
            item.nombre_registro = str(item.name[indice_inicial:indice_final])