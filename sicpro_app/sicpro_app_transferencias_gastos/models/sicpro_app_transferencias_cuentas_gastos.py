# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint
from odoo import fields, models, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class TransferenciasCuentasGastos(models.Model):
    _name = 'sicpro.app.transferencias.cuentas.gastos'
    _description = 'Cuentas de Gastos de las transferencias'

    @api.model
    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Cuenta', required=True)
    descripcion = fields.Char(string='Descripción', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    color = fields.Integer(string='Color', default=_default_color)
    traspasos = fields.Boolean(string='Traspasos', required=False,
                               default=False,
                               help='Esta cuenta siempre es negativa. Es la que se utiliza para traspasarlos '
                                    'gastos a los territorios.')
    company_id = fields.Many2one('res.company', string='Compañía',
        required=True, default=lambda self: self.env.company,
        help='Compañía a la que pertenece esta cuenta de gasto')
    company_currency = fields.Many2one('res.currency',
        string='Moneda de la Compañía', related='company_id.currency_id',
        readonly=True, store=True,
        help='Moneda principal de la compañía asignada')

    @api.constrains('name')
    def _check_name_control_unique(self):
        for record in self:
            domain = [('name', '=', record.name), ('id', '!=', record.id)]

            if self.env[
                'sicpro.app.transferencias.cuentas.gastos'].search_count(
                domain) > 0:
                raise ValidationError(
                    "¡El nombre de la cuenta '%s' ya existe en el sistema!.\n\n" % record.name + MSG_SOPORTE_SICPRO)

    def copy(self, default=None):
        """
        Sobrescribe la duplicación para asegurar que el código de la cuenta mantenga unicidad.
        """
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = f"{self.name} (Copia)"
        return super(TransferenciasCuentasGastos, self).copy(default)