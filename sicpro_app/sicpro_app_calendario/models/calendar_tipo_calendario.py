# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


Prioridades_Activas = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'), ('3', 'Muy Alta'), ]


class MeetingTipoCalendario(models.Model):
    _name = 'calendar.tipo.calendario'
    _description = 'Tipo de Calendario'

    name = fields.Char('Nombre', required=True)
    plantilla_impresion = fields.Boolean(string='Impresión', required=False, default=False)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    prioridad = fields.Selection(Prioridades_Activas, string='Prioridad', index=True, default=Prioridades_Activas[0][0])
    tipo_defecto = fields.Boolean(string='Por defecto', required=False, default=False)
    tipo_dvpe = fields.Boolean(string='Inf. DVPE', required=False, default=False)
    tipo_desarrollo = fields.Boolean(string='Inf. Desarrollo', required=False, default=False)

    _sql_constraints = [('name_uniq', 'unique (name)', "¡El tipo de actividad de calendario existe!"), ]

    @api.constrains('tipo_defecto')
    def _check_tipo_defecto(self):
        check_datos = self.env['calendar.tipo.calendario'].search([('tipo_defecto', '=', True), ])
        cuenta = 0
        for item in check_datos:
            cuenta += len(item)

        if cuenta > 1:
            raise ValidationError(_('¡Solo puede existir un valor por defecto, verifíquelo!.'))
