# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO


class TransporteTipoCombustible(models.Model):
    _name = 'sicpro.app.transporte.tipo.combustible'
    _description = 'Tipo de Combustible para el Transporte'
    _order = 'name asc'

    name = fields.Char(string='Nombre', required=True)
    categoria = fields.Selection(string='Categoría', required=True,
        default='diesel',
        selection=[('diesel', 'Diesel'), ('especial', 'Especial'),
                   ('regular', 'Regular')])
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Moneda', readonly=True,
                                       related='company_id.currency_id')
    costo = fields.Monetary(string='Costo', required=True,
                            currency_field='company_currency')

    @api.constrains('name')
    def _check_name_control_unique(self):
        for record in self:
            domain = [('name', '=', record.name), ('id', '!=', record.id)]

            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡El tipo de combustible '%s' ya existe en el sistema!" % record.name + MSG_SOPORTE_SICPRO)
