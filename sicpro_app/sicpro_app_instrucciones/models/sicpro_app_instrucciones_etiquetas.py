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


class InstruccionesEtiquetas(models.Model):
    _name = 'sicpro.app.instrucciones.etiquetas'
    _description = 'Etiquetas de las Instrucciones'

    name = fields.Char(string='Etiqueta', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, index=True)

    @api.constrains('name')
    def _check_unique_tag_name(self):
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError(
                    "El nombre de la etiqueta no puede estar vacío.\n\n" + MSG_SOPORTE_SICPRO)

            name_clean = record.name.strip()
            duplicate = self.search(
                [('name', '=ilike', name_clean), ('id', '!=', record.id)],
                limit=1)

            if duplicate:
                raise ValidationError(
                    "¡Conflicto de Etiquetas! El nombre '%s' ya está en uso." % name_clean + MSG_SOPORTE_SICPRO)
