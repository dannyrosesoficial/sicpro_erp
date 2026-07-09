# -*- coding: utf-8 -*-

from random import randint

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class CorreosEntrantesMetodos(models.Model):
    _name = 'sicpro.modulo.base.correos.entrantes.metodos'
    _description = 'Métodos a ejecutar en la entrada de un correo'

    asunto = fields.Many2many('sicpro.modulo.base.correos.entrantes.asuntos',
                              'sicpro_modulo_base_correos_entrantes_asuntos_rel',
                              string='Asunto del correo', required=True,)
    active = fields.Boolean(string="Activo", default=True, )
    name = fields.Selection([], string="Modelo - Método", required=True, )
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    # verífico que no se repita el método en el registro
    @api.constrains('name')
    def _check_metodo_correo_unico(self):
        uniq = self.env['sicpro.modulo.base.correos.entrantes.metodos'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡El Método de automatización seleccionado, "
                                    "ya cuenta con un asunto de correo con la misma descripción!. "
                                    "Si cree que es un error contacte al administrador"))
