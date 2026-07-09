# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class MeetingCargosExternos(models.Model):
    _name = 'calendar.cargos.externos'
    _description = 'Cargo Externos del Calendario'

    name = fields.Char('Cargo', required=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    active = fields.Boolean(string='Archivado', required=True, default=True)

    @api.constrains('name')
    def _check_actividades_unico(self):
        uniq = self.env['calendar.cargos.externos'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡El cargo introducido ya existe!. "
                                    "Si cree que es un error contacte al administrador"))
