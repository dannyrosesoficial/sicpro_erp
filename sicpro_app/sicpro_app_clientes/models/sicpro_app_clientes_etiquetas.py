# -*- coding: utf-8 -*-


from odoo import fields, models, api


class AppClientesEtiquetas(models.Model):
    _name = 'sicpro.app.clientes.etiquetas'
    _order = "id asc"
    _description = 'Etiquetas para la Aplicación de Clientes'

    name = fields.Char('Etiqueta', required=True)
    color = fields.Integer(string='Color Index', copy=False,
                           readonly=True, index=True, )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"),
    ]

    # Crear la secuencia de incremento en el campo color, asignado el rango de colores automaticamente
    @api.model
    def create(self, vals):
        vals['color'] = self.env['ir.sequence'].next_by_code(
            'clientes_etiquetas_incrementar')
        res = super(AppClientesEtiquetas, self).create(vals)
        return res
