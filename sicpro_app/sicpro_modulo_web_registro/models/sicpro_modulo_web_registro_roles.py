# -*- coding: utf-8 -*-

from odoo import fields, models


class SicproWebRoles(models.Model):
    _name = 'sicpro.modulo.web.registro.roles'
    _description = 'Roles para el registro de usuarios'
    _order = "sequence, id"

    name = fields.Char('Nombre', required=True)
    sequence = fields.Integer('Secuencia', default=1, )
    active = fields.Boolean(string='Archivado', default=True)
    descripcion = fields.Char(string='Descripción', required=True)
    roles = fields.Many2many('sicpro.modulo.roles', 'web_registro_roles_acceso_rel', string='Roles', required=True)
