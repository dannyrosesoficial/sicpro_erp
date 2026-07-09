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


def _default_color():
    return randint(1, 11)


class TransferenciasCuentasGastos(models.Model):
    _name = 'sicpro.app.transferencias.cuentas.gastos'
    _description = 'Cuentas de Gastos de las transferencias'

    name = fields.Char(string='Cuenta', required=True)
    descripcion = fields.Char(string='Descripción', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    color = fields.Integer(string='Color', default=_default_color)
    traspasos = fields.Boolean(string='Traspasos', required=False,
                               default=False,
                               help='Esta cuenta siempre es negativa. Es la que se utiliza para traspasarlos '
                                    'gastos a los territorios.')

    @api.constrains('name')
    def _check_name_control_unique(self):
        for record in self:
            domain = [('name', '=', record.name), ('id', '!=', record.id)]

            if self.env[
                'sicpro.app.transferencias.cuentas.gastos'].search_count(
                domain) > 0:
                raise ValidationError(
                    "¡El nombre de la cuenta '%s' ya existe en el sistema!.\n\n" % record.name + MSG_SOPORTE_SICPRO)
