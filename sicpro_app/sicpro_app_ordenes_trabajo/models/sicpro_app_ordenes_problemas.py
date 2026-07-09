# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO


class OrdenesProblemas(models.Model):
    _name = 'sicpro.app.ordenes.problemas'
    _description = 'Problemas en la ejecución'

    name = fields.Char(string='Descripción', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)

    @api.constrains('name')
    def _check_name_uniqueness(self):
        """ Garantiza que no se dupliquen las descripciones de los problemas de ejecución """
        for record in self:
            if record.name:
                duplicate = self.search(
                    [('name', '=', record.name), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError(
                        f"¡La descripción del problema '{record.name}' ya se encuentra registrada en el sistema!\n\n"
                        f"{MSG_SOPORTE_SICPRO}")