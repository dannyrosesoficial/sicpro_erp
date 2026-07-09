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


class MeetingActividadesOrganizativas(models.Model):
    _name = 'calendar.actividades.organizativas'
    _description = 'Actividades Organizativas del Calendario'

    name = fields.Char(string='Actividades', required=True)
    usuarios_ids = fields.Many2many('res.users', string="Usuarios",
                                    readonly=False, store=True, )
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string='Archivado', required=True, default=True, index=True)

    @api.constrains('name')
    def _check_actividades_unico(self):
        uniq = self.env['calendar.actividades.organizativas'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name),
             ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(
                "¡La actividad introducida ya existe!.\n\n" + MSG_SOPORTE_SICPRO)
