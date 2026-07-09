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
from odoo.exceptions import ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO

def _default_color():
    return randint(1, 11)


class ProductosEtiquetas(models.Model):
    _name = "sicpro.app.materiales.insumos.etiquetas"
    _description = "Etiquetas de los productos"

    name = fields.Char(string='Nombre de la etiqueta', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    @api.constrains('name')
    def _check_unique_tag_name(self):
        for record in self:
            if record.name:
                # Limpiamos espacios y buscamos sin importar mayúsculas
                # Esto evita que 'Urgente' y 'urgente' coexistan
                name_clean = record.name.strip()
                duplicate = self.search([
                    ('name', '=ilike', name_clean),
                    ('id', '!=', record.id)
                ], limit=1)

                if duplicate:
                    raise ValidationError("¡Conflicto de Etiquetas! El nombre '%s' ya está en uso. "
                        "Por favor, elija un nombre de etiqueta único para SICPRO.\n\n" % name_clean + MSG_SOPORTE_SICPRO)
