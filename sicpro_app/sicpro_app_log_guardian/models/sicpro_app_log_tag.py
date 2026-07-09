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


def _default_color():
    return randint(1, 11)

class SicproLogTag(models.Model):
    _name = 'sicpro.log.tag'
    _description = 'Etiquetas de Log'

    name = fields.Char(string="Nombre", required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            domain = [('name', '=', record.name), ('id', '!=', record.id)]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡El nombre de la etiqueta existe!\n\n" + MSG_SOPORTE_SICPRO)
