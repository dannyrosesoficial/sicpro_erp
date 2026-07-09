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


def _default_color():
    return randint(1, 11)


class ReunionesLugares(models.Model):
    _name = 'sicpro.app.reuniones.lugares'
    _description = 'Lugares de las Reuniones'

    # Crear la secuencia de incremento en el campo color.

    name = fields.Char(string='Lugar', required=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=False)
    descripcion = fields.Char(string='Descripción', )
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    tipo = fields.Selection(string='Tipo', selection=[('interno', 'Interno'), (
    'externo', 'Externo'), ], required=True, )

    @api.constrains('name')
    def _check_name_control_unique(self):
        for record in self:
            domain = [('name', '=', record.name), ('id', '!=', record.id)]

            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡El nombre del lugar '%s' ya existe en el "
                    "sistema!\n\n" % record.name + MSG_SOPORTE_SICPRO)
