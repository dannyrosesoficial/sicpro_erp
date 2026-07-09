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


class ViviendaMaterialesUM(models.Model):
    _name = 'sicpro.app.vivienda.materiales.um'
    _description = 'Unidad de medidas de los materiales'

    name = fields.Char(string='U/M', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    @api.constrains('name')
    def _check_unique_uom_name(self):
        for record in self:
            if record.name:
                name_clean = record.name.strip()

                duplicate = self.search(
                    [('name', '=ilike', name_clean), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError(
                        "¡Error de Configuración! La unidad de medida '%s' ya existe. "
                        "Por favor, use la unidad existente para mantener la integridad de los cálculos." % name_clean + MSG_SOPORTE_SICPRO)
