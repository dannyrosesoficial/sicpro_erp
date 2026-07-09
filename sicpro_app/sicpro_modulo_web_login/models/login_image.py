# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LoginImage(models.Model):
    _name = 'sicpro.modulo.web.login.imagen'
    _description = 'Imagen del Login'
    _rec_name = 'name'

    image = fields.Binary(string="Imagen")
    name = fields.Char(string="Nombre")
    mantenimiento = fields.Boolean(string='Modo Mantenimiento', required=False, default=False)

    # verífico que no se repita la imagen de mantenimiento, solo puede existir una
    @api.constrains('mantenimiento')
    def _check_mantenimiento_unico(self):
        uniq = self.env['sicpro.modulo.web.login.imagen'].search([("mantenimiento", "=", True)])
        valor = len(uniq)
        if valor > 1:
            raise ValidationError(_("¡Ya existe una imagen para el modo de mantenimiento!. "
                                    "Si cree que es un error contacte al administrador"))
