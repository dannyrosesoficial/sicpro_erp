# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint
from odoo import fields, models, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class ControlInformacionDias(models.Model):
    _name = "sicpro.app.control.informacion.dias"
    _description = "Días de aviso para el control de información"

    name = fields.Integer(string='Día', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string='Activo', default=True, index=True)

    @api.constrains('name')
    def _check_area_unica(self):
        uniq = self.env['sicpro.app.control.informacion.dias'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name),
             ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(
                "¡El día introducido ya existe!.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            for item in self:
                if item.name < 1 or item.name > 20:
                    raise ValidationError(
                        "Los días para notificar no puede ser inferiores a 1 o superiores a 20.\n\n" + MSG_SOPORTE_SICPRO)