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


class OrdenesProgramaInversiones(models.Model):
    _name = 'sicpro.app.ordenes.programa.inversiones'
    _description = 'Programa de Inversiones de las Órdenes de Trabajo'

    name = fields.Char(string='Descripción', required=True)
    plan = fields.Char(string='Plan', required=True)
    consecutivo = fields.Integer(string='Consecutivo', required=True,
                                 default=1)
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor',
                                 domain="[('ejecuta_proceso', '=', True)]",
                                 required=True, )
    company_abreviatura = fields.Char(string='Abreviatura',
                                      related='company_id.identificador_corto')

    active = fields.Boolean(string='Activo', default=True, index=True)

    @api.constrains('plan', 'consecutivo', 'company_id')
    def _check_consecutivo_unico(self):
        """ Evita duplicar el mismo número consecutivo o plan dentro del mismo proceso ejecutor """
        for record in self:
            if record.company_id and record.plan:
                duplicate = self.search([('plan', '=', record.plan),
                    ('consecutivo', '=', record.consecutivo),
                    ('company_id', '=', record.company_id.id),
                    ('id', '!=', record.id)], limit=1)

                if duplicate:
                    raise ValidationError(
                        f"¡Conflicto de secuencia en SICPRO!\n\n"
                        f"El plan '{record.plan}' con el consecutivo #{record.consecutivo} "
                        f"ya se encuentra asignado al proceso ejecutor '{record.company_id.name}'.\n\n"
                        f"{MSG_SOPORTE_SICPRO}")