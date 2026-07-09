# -*- coding: utf-8 -*-


from odoo import fields, models, api


class TransporteEtiquetas(models.Model):
    _name = 'sicpro.app.transporte.etiqueta'
    _description = 'Etiquetas del transporte'

    name = fields.Char('Nombre de etiqueta', required=True, translate=True)
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
            'transporte_etiquetas_incrementar')
        res = super(TransporteEtiquetas, self).create(vals)
        return res
