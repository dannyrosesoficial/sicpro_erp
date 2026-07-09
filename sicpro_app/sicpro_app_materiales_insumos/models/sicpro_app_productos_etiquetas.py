# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductosEtiquetas(models.Model):
    _name = "sicpro.app.materiales.insumos.etiquetas"
    _description = "Etiquetas de los productos"

    name = fields.Char('Nombre de la etiqueta', required=True, translate=True)
    color = fields.Integer(string='Color Index', copy=False,
                           readonly=True, index=True, )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]

    # Crear la secuencia de incremento en el campo color, asignado el rango
    # de colores automáticamente
    @api.model
    def create(self, vals):
        vals['color'] = self.env['ir.sequence'].next_by_code(
            'materiales_insumos_etiquetas_incrementar')
        res = super(ProductosEtiquetas, self).create(vals)
        return res

