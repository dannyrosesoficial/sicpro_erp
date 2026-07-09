# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ContratosEtiquetas(models.Model):
    _name = 'sicpro.app.contratos.etiquetas'
    _description = 'Etiquetas de los contratos'

    name = fields.Char('Etiqueta', required=True)
    color = fields.Integer(string='Color Index', copy=False,
                           readonly=True, index=True, )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]

    # Crear la secuencia de incremento en el campo color, asignado el rango
    # de colores automáticamente e
    @api.model
    def create(self, vals):
        vals['color'] = self.env['ir.sequence'].next_by_code(
            'contratos_etiquetas_incrementar')
        res = super(ContratosEtiquetas, self).create(vals)
        return res
