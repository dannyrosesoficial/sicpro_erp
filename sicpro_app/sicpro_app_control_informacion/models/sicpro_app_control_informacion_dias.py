# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class ControlInformacionDias(models.Model):
    _name = "sicpro.app.control.informacion.dias"
    _description = "Días de aviso para el control de información"

    name = fields.Integer('Día', required=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    active = fields.Boolean('Activo', default=True)

    @api.constrains('name')
    def _check_area_unica(self):
        uniq = self.env['sicpro.app.control.informacion.dias'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡El día introducido ya existe!. "
                                    "Si cree que es un error contacte al administrador"))
        else:
            for item in self:
                if item.name < 1 or item.name > 20:
                    raise ValidationError(_('Los días para notificar no puede ser inferiores a 1 o superiores a 20.'))
