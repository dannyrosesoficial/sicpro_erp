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


class NomencladorCentroCosto(models.Model):
    _name = 'sicpro.nomenclador.centro.costo'
    _description = 'Nomenclador de Centros de Costos'

    name = fields.Char(string='Centro Costo', required=True)
    descripcion = fields.Char(string='Descripción', required=False)
    company_id = fields.Many2one(comodel_name="res.company", string="Proceso",
                                 required=True)
    area_empresa_id = fields.Many2one(
        comodel_name="sicpro.nomenclador.areas.empresa",
        string="Área de Empresa")
    active = fields.Boolean(string="Activo", default=True, index=True)

    @api.constrains('name')
    def _check_unique_cost_center(self):
        for record in self:
            if record.name:
                name_clean = record.name.strip()
                duplicate = self.search(
                    [('name', '=ilike', name_clean), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError(
                        "¡Conflicto Contable! El Centro de costo '%s' ya existe. "
                        "Por favor, verifique el listado en SICPRO para evitar duplicidad.\n\n" % name_clean + MSG_SOPORTE_SICPRO)
