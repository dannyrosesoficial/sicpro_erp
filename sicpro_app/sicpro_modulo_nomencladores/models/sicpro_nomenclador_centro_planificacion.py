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


class NomencladorCentroPlanificacion(models.Model):
    _name = 'sicpro.nomenclador.centro.planificacion'
    _description = 'Nomenclador de Centros de Planificación (CePl)'

    name = fields.Char(string='CePl', required=True)
    descripcion = fields.Char(string="Descripción", required=True)
    active = fields.Boolean(string="Activo", default=True, index=True)

    @api.constrains('name')
    def _check_unique_planning_center(self):
        for record in self:
            if record.name:
                name_clean = record.name.strip()
                duplicate = self.search(
                    [('name', '=ilike', name_clean), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError(
                        "¡Atención! El Centro de Planificación '%s' ya está registrado en el sistema."
                        "Por favor, verifique los datos para evitar duplicidades.\n\n" % name_clean + MSG_SOPORTE_SICPRO)
