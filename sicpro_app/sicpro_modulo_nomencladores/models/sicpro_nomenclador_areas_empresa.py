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


class NomencladorAreasEmpresa(models.Model):
    _name = 'sicpro.nomenclador.areas.empresa'
    _description = 'Nomenclador de Área de Empresa'

    name = fields.Integer(string='Área de Empresa', required=True)
    descripcion = fields.Char(string="Descripción", required=True)
    active = fields.Boolean(string="Activo", default=True, index=True)

    @api.constrains('name')
    def _check_unique_area_name(self):
        for record in self:
            name_text = str(record.name).strip() if record.name else ""
            if not name_text:
                continue

            duplicate = self.search(
                [('name', '=ilike', name_text), ('id', '!=', record.id)],
                limit=1)

            if duplicate:
                raise ValidationError(
                    "¡Conflicto de Estructura! El Área de Empresa '%s' ya se encuentra registrada. "
                    "Por favor, use un nombre distintivo para el área.\n\n" % name_text + MSG_SOPORTE_SICPRO)
