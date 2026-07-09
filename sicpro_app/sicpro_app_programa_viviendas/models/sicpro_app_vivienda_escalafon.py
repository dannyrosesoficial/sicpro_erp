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


class ViviendaEscalafon(models.Model):
    _name = "sicpro.app.vivienda.escalafon"
    _description = "Escalafón del programa de la vivienda"

    name = fields.Integer(string='Número', required=True)

    @api.constrains('name')
    def _check_unique_escalafon(self):
        for record in self:
            if record.name:
                duplicate = self.search(
                    [('name', '=', record.name), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError(
                        "¡Error de Escalafón! El número '%s' ya está asignado a otro registro. "
                        "Cada trabajador debe tener un número de escalafón único.\n\n" % record.name + MSG_SOPORTE_SICPRO)
