# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint

from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class TrabajadoresFamiliar(models.Model):
    _name = "sicpro.app.trabajadores.familiar"
    _description = "Relaciones de los familiares del trabajador"

    name = fields.Char(string="Relación", required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            # Buscamos si existe otro registro con el mismo nombre
            domain = [('name', '=', record.name), ('id', '!=', record.id)]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡El nombre de la relación '%s' ya existe en el sistema!" % record.name + MSG_SOPORTE_SICPRO)
