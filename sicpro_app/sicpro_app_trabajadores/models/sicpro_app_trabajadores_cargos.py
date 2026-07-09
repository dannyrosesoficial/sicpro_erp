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


class TrabajadoresCargos(models.Model):
    _name = 'sicpro.app.trabajadores.cargos'
    _description = 'Cargos del Trabajador'

    name = fields.Char(string='Cargo del Trabajador', required=True,
                       index=True, )
    descripcion = fields.Text(string='Descripción de la categoría')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    salario = fields.Monetary(string="Salario", currency_field='company_currency_id',
                              required=True)
    alimentacion = fields.Monetary(string="Alimentación", required=True,
                                   currency_field='company_currency_id')
    active = fields.Boolean(string='Activo', default=True, index=True)

    @api.constrains('name')
    def _check_unique_cargo_name(self):
        for record in self:
            # Buscamos si existe otro cargo con el mismo nombre
            domain = [('name', '=', record.name), ('id', '!=', record.id)]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡Error! El cargo '%s' ya está registrado en el sistema." % record.name + MSG_SOPORTE_SICPRO)
