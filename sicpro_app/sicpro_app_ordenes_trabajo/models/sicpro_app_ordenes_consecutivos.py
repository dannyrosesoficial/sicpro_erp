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
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO


class OrdenesProgramaConsecutivos(models.Model):
    _name = 'sicpro.app.ordenes.consecutivos'
    _description = 'Programa de Inversiones de las Órdenes de Trabajo'

    name = fields.Char(string='Nomenclador', required=True)
    moneda = fields.Char(string='Moneda', required=True)
    tipo = fields.Selection(string='Tipo de Orden',
                            selection=[('inversiones', 'Inversiones'),
                                       ('mantenimiento', 'Mantenimiento'), ],
                            required=True)
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor',
                                 domain="[('ejecuta_proceso', '=', True)]",
                                 required=True)
    company_abreviatura = fields.Char(string='Abreviatura', required=False,
                                      related='company_id.identificador_corto')
    active = fields.Boolean(string='Activo', default=True, index=True)

    @api.constrains('name')
    def _check_name_uniqueness(self):
        for record in self:
            if record.name:
                duplicate = self.search(
                    [('name', '=', record.name), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError(
                        "El identificador de consecutivos ya existe.\n\n" +
                        MSG_SOPORTE_SICPRO)