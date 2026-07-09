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


class Municipality(models.Model):
    _name = 'res.municipality'
    _description = 'Municipio'
    _order = 'code'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código', help='El código del municipio', required=True)
    country_id = fields.Many2one('res.country', string='Pais',
                                 default='base.cu', required=True)
    state_id = fields.Many2one('res.country.state', 'Provincia',
                               domain="[('country_id', '=', country_id)]")

    @api.constrains('state_id', 'code')
    def _check_unique_municipio_code(self):
        for record in self:
            # Buscamos si ya existe el mismo código en la misma provincia
            if record.state_id and record.code:
                domain = [('state_id', '=', record.state_id.id),
                    ('code', '=', record.code.strip()),
                    ('id', '!=', record.id)]
                if self.search_count(domain) > 0:
                    raise ValidationError(
                        "¡Error de Codificación! El código '%s' ya está asignado a otro municipio "
                        "en la provincia de '%s'. Por favor, asigne un código único." % (
                        record.code,
                        record.state_id.name) + MSG_SOPORTE_SICPRO)
