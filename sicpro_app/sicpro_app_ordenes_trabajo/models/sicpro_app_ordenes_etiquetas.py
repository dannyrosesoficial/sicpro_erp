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
from odoo.exceptions import ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO


def _default_color():
    return randint(1, 11)


class OrdenesEtiquetas(models.Model):
    _name = "sicpro.app.ordenes.etiquetas"
    _description = "Etiquetas de las órdenes de trabajo"

    name = fields.Char(string='Nombre de la etiqueta', required=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    @api.constrains('name')
    def _check_name_control_unique(self):
        for record in self:
            domain = [('name', '=', record.name), ('id', '!=', record.id)]

            if self.search_count(domain) > 0:
                raise ValidationError(
                    f"¡El nombre de la etiqueta '{record.name}' ya existe en el sistema!\n\n"
                    f"{MSG_SOPORTE_SICPRO}"
                )