# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models,api


class ResUsersWebRoles(models.Model):
    _inherit = "res.users.role"

    nombre_registro = fields.Char(string='Nombre de registro', compute='_compute_nombre_rol', store=True)

    # género el nombre del rol que aparecerá en el registro del usuario
    @api.depends('name')
    def _compute_nombre_rol(self):
        for item in self:
            # 1. Protección contra valores nulos (False)
            if not item.name:
                item.nombre_registro = ""
                continue

            # 2. Buscar el índice del separador
            indice = item.name.find(':')

            if indice != -1:
                # Usamos slicing de Python [inicio:] que es más seguro
                # +1 para saltar el ':' y .strip() para quitar espacios sobrantes
                res = item.name[indice + 1:].strip()
                item.nombre_registro = str(res)
            else:
                # Si no hay ':', devolvemos el nombre completo
                item.nombre_registro = str(item.name)