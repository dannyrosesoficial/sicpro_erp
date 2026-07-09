# -*- coding: utf-8 -*-

from odoo import fields, models


class MeetingPieFirmas(models.Model):
    _name = 'calendar.pie.firmas'
    _description = 'Pie de Firma del Calendario'

    name = fields.Many2one('res.users', string='Usuario', required=True)
    tipo = fields.Selection(string='Tipo', selection=[('aprueba', 'Aprueba'), ('elabora', 'Elabora'), ], required=True,)
    active = fields.Boolean(string='Archivado', required=True, default=True)

    _sql_constraints = [('tipo_uniq', 'unique (tipo)', "¡El tipo de autorización existe!"), ]
