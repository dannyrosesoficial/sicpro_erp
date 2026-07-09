# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint

from odoo import models, fields, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class DesactivarUsuarioDias(models.Model):
    _name = 'sicpro.app.modulo.usuario.desactivar.dias'
    _description = 'Aviso en días para la desactivación de los usuarios'
    _order = "id asc"

    name = fields.Integer(string='Días', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            # Buscamos si existe otro registro con el mismo nombre (excluyendo el actual)
            domain = [('name', '=', record.name), ('id', '!=', record.id)]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡El día ya existe!\n\n" + MSG_SOPORTE_SICPRO)
