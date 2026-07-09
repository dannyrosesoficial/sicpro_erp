# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class State(models.Model):
    _inherit = 'res.country.state'

    res_municipality_id = fields.Many2one('res.municipality', 'Municipio',
        help="Municipios de Cuba")
    abreviatura = fields.Char(string="Abreviatura", required=False)

    def _check_abreviatura_obligatoria(self):
        for record in self:
            # Si el país es Cuba (puedes usar el ID o el código del país)
            # Generalmente el código de Cuba en Odoo es 'CU'
            if record.country_id.code == 'CU' and not record.abreviatura:
                raise ValidationError(
                    "La abreviatura es obligatoria para las provincias de Cuba.")
