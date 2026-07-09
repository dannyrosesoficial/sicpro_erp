# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo import models, fields, api
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class TransferenciasGastosOrdenesMorosidad(models.Model):
    _name = "sicpro.app.transferencias.gastos.ordenes.morosidad"
    _description = "Periodo de tiempo en que se debe recibir la certificación de gastos"
    _order = "sequence asc"

    name = fields.Integer(string='Periodo (días)', required=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor',
                                 domain="[('ejecuta_proceso', '=', True)]",
                                 required=True,
                                 default=lambda self: self.env.company)
    company_abreviatura = fields.Char(string='Abreviatura', required=False,
                                      related='company_id.identificador_corto')
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    @api.constrains('company_id')
    def _check_name_control_unique(self):
        for record in self:
            domain = [('company_id', '=', record.company_id.id),
                      ('id', '!=', record.id)]

            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡El nombre del proceso '%s' ya existe en el "
                    "sistema!.\n\n" % record.company_id.name + MSG_SOPORTE_SICPRO)