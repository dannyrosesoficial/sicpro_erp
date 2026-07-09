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


class NomencladorDepartamentos(models.Model):
    _name = 'sicpro.nomenclador.departamentos'
    _description = 'Nomenclador Departamentos del Proceso'
    _order = 'sequence, id'

    name = fields.Char(required=True, string='Departamento')
    company_id = fields.Many2one(comodel_name="res.company", string="Proceso",
                                 required=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    active = fields.Boolean(string="Activo", default=True, index=True)

    @api.constrains('name', 'company_id')
    def _check_unique_department_per_company(self):
        for record in self:
            if record.name:
                domain = [('name', '=ilike', record.name.strip()),
                    ('company_id', '=', record.company_id.id),
                    ('id', '!=', record.id)]
                if self.search_count(domain) > 0:
                    raise ValidationError(
                        "¡Error de Organización! El departamento '%s' ya existe "
                        "para la compañía '%s'. No se permiten duplicados en el mismo proceso.\n\n" % (
                        record.name,
                        record.company_id.name) + MSG_SOPORTE_SICPRO)
