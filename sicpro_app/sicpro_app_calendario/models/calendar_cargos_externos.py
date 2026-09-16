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


class MeetingCargosExternos(models.Model):
    _name = 'calendar.cargos.externos'
    _description = 'Cargo Externos del Calendario'

    @api.model
    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Cargo', required=True)
    color = fields.Integer(string='Color',
                           default=_default_color)
    active = fields.Boolean(string='Archivado', required=True, default=True, index=True)

    @api.constrains('name')
    def _check_actividades_unico(self):
        uniq = self.env['calendar.cargos.externos'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name),
             ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(
                "¡El cargo introducido ya existe!.\n\n" + MSG_SOPORTE_SICPRO)
