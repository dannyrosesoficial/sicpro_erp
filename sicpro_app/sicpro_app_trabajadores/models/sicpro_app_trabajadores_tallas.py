# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint

from odoo import api, models, fields
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class TrabajadoresTallas(models.Model):
    _name = "sicpro.app.trabajadores.tallas"
    _description = "Tallas de los trabajadores"

    name = fields.Char(string="Nombre de la etiqueta", required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    @api.constrains('name')
    def _check_unique_talla_name(self):
        for record in self:
            # Usamos =ilike para que "M" y "m" se consideren duplicados
            # y .strip() para ignorar espacios accidentales
            duplicate = self.search([('name', '=ilike', record.name.strip()),
                ('id', '!=', record.id)], limit=1)

            if duplicate:
                raise ValidationError(
                    "¡Error de Inventario! La talla '%s' ya está registrada en SICPRO. "
                    "Por favor, verifique la lista de tallas existentes." % record.name + MSG_SOPORTE_SICPRO)
