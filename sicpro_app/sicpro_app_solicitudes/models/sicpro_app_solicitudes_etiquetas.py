# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint
from odoo.exceptions import ValidationError
from odoo import fields, models, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO


def _default_color():
    return randint(1, 11)


class SolicitudesEtiquetas(models.Model):
    _name = "sicpro.app.solicitudes.etiquetas"
    _description = "Etiquetas de las Solicitudes"

    name = fields.Char(string='Nombre de la etiqueta', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            exist = self.search(
                [('name', '=', record.name), ('id', '!=', record.id)], limit=1)

            if exist:
                raise ValidationError(
                    "¡El nombre de la etiqueta '%s' ya existe! " % record.name + MSG_SOPORTE_SICPRO)