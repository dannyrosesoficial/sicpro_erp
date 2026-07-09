# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class PreparacionTecnicaEtiquetas(models.Model):
    _name = "sicpro.app.preparacion.tecnica.etiquetas"
    _description = "Etiquetas de la Preparacion Tecnica"

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
            'preparacion_tecnica_etiquetas_incrementar')
        res = super(PreparacionTecnicaEtiquetas, self).create(vals)
        return res
