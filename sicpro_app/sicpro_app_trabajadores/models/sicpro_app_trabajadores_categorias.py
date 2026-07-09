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


class TrabajadoresCategorias(models.Model):
    _name = "sicpro.app.trabajadores.categorias"
    _description = "Etiquetas de los trabajadores"

    name = fields.Char(string="Nombre de la etiqueta", required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    tipo = fields.Selection(string='Tipo', required=True,
                            selection=[('contrato', 'Clase de Contrato'), (
                            'ocupacional', 'Categoría Ocupacional'), ], )

    @api.constrains('name')
    def _check_unique_tag_name(self):
        for record in self:
            # Buscamos registros con el mismo nombre, excluyendo el actual
            duplicate = self.search(
                [('name', '=', record.name), ('id', '!=', record.id)], limit=1)

            if duplicate:
                raise ValidationError(
                    "¡Atención! La etiqueta '%s' ya existe. No se permiten nombres duplicados." % record.name + MSG_SOPORTE_SICPRO)
