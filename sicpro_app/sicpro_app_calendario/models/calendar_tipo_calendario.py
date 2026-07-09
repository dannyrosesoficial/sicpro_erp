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


PRIORIDADES_ACTIVAS = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'),
                       ('3', 'Muy Alta'), ]


class MeetingTipoCalendario(models.Model):
    _name = 'calendar.tipo.calendario'
    _description = 'Tipo de Calendario'

    name = fields.Char(string='Nombre', required=True)
    plantilla_impresion = fields.Boolean(string='Impresión', required=False,
                                         default=False)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    prioridad = fields.Selection(PRIORIDADES_ACTIVAS, string='Prioridad',
                                 index=True, default=PRIORIDADES_ACTIVAS[0][0])
    tipo_defecto = fields.Boolean(string='Por defecto', required=False,
                                  default=False)
    tipo_dvpe = fields.Boolean(string='Inf. DVPE', required=False,
                               default=False)
    tipo_desarrollo = fields.Boolean(string='Inf. Desarrollo', required=False,
                                     default=False)

    @api.constrains('name')
    def _check_unique_activity_type(self):
        for record in self:
            if record.name:
                # Buscamos duplicados ignorando mayúsculas/minúsculas y espacios accidentales
                name_clean = record.name.strip()
                duplicate = self.search(
                    [('name', '=ilike', name_clean), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError(
                        "¡Error de Calendario! El tipo de actividad '%s' ya existe. "
                        "Por favor, verifique la lista para no crear categorías duplicadas.\n\n" % name_clean + MSG_SOPORTE_SICPRO)

    @api.constrains('tipo_defecto')
    def _check_tipo_defecto(self):
        check_datos = self.env['calendar.tipo.calendario'].search(
            [('tipo_defecto', '=', True), ])
        cuenta = 0
        for item in check_datos:
            cuenta += len(item)

        if cuenta > 1:
            raise ValidationError(
                '¡Solo puede existir un valor por defecto, verifíquelo!.' + MSG_SOPORTE_SICPRO)
