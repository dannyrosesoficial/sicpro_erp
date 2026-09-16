# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api
from random import randint
from odoo.exceptions import ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO


class SalonClasesTipo(models.Model):
    _name = "sicpro.app.salon.clases.tipo"
    _description = "Tipo de temáticas"

    @api.model
    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Nombre', required=True)
    color = fields.Integer(string='Color',
                           default=_default_color)

    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            domain = [('name', '=', record.name), ('id', '!=', record.id)]
            if self.search_count(domain) > 0:
                raise ValidationError("¡El nombre de la temáticas existe!\n\n\n\n" + MSG_SOPORTE_SICPRO)