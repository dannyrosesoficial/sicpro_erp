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


class NomencladorEmplazamientos(models.Model):
    _name = 'sicpro.nomenclador.emplazamientos'
    _description = 'Nomenclador de Emplazamientos'

    name = fields.Char(string='Emplazamiento', required=True)
    centro_planificacion = fields.Many2one(string='Centro Planificación',
                                           required=True,
                                           comodel_name='sicpro.nomenclador.centro.planificacion')
    active = fields.Boolean(string="Activo", default=True, index=True)

    @api.constrains('name')
    def _check_unique_cost_center_name(self):
        for record in self:
            domain = [('name', '=ilike', record.name.strip()),
                ('id', '!=', record.id)]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡Conflicto de Contabilidad! El Centro de costo '%s' ya existe en el sistema. "
                    "Por favor, verifique el nombre o use uno diferente.\n\n" % record.name + MSG_SOPORTE_SICPRO)
