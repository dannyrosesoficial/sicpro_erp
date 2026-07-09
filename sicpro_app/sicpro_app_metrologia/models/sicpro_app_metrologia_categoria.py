# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MetrologiaCategoria(models.Model):
    _name = 'sicpro.app.metrologia.categoria'
    _description = 'Categorías del Mantenimiento de Equipos'

    name = fields.Char('Nombre', required=True)
    notas = fields.Text('Comentarios')
    vigencia = fields.Integer(string='Vigencia (Años)', required=True)
    dias = fields.Integer(string='Días', required=False,
                          compute='_compute_dias_vigencia')

    @api.depends('vigencia')
    def _compute_dias_vigencia(self):
        for vigencia in self:
            if vigencia.vigencia:
                vigencia.dias = vigencia.vigencia * 365
            else:
                vigencia.dias = None
