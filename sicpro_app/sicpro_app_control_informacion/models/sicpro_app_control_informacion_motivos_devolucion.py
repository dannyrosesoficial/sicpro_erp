# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, models, fields
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class ControlInformacionMotivosRechazos(models.Model):
    _name = "sicpro.app.control.informacion.motivos.devolucion"
    _description = "Motivos de rechazo del control de información"

    name = fields.Char(string='Motivo', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)

    @api.constrains('name')
    def _check_unique_rejection_reason(self):
        for record in self:
            if record.name:
                name_clean = record.name.strip()
                duplicate = self.search(
                    [('name', '=ilike', name_clean), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError(
                        "¡Registro Duplicado! El motivo de rechazo '%s' ya existe en el sistema. "
                        "Por favor, seleccione el motivo existente o use un nombre diferente.\n\n" % name_clean + MSG_SOPORTE_SICPRO)