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


class OrdenesParalizacion(models.Model):
    _name = 'sicpro.app.ordenes.paralizacion'
    _description = 'Motivo de la última paralización'

    name = fields.Char(string='Motivo', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)

    @api.constrains('name')
    def _check_name_uniqueness(self):
        """ Garantiza que no se dupliquen las razones o motivos de paralización """
        for record in self:
            if record.name:
                duplicate = self.search(
                    [('name', '=', record.name), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError(
                        f"¡El motivo de paralización '{record.name}' ya se encuentra registrado en el sistema!\n\n"
                        f"{MSG_SOPORTE_SICPRO}")