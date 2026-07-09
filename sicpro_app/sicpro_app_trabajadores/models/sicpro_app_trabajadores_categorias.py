# -*- coding: utf-8 -*-

from odoo import fields, models, api


class TrabajadoresEtiquetas(models.Model):
    _name = "sicpro.app.trabajadores.categorias"
    _description = "Categorias de los trabajadores"

    name = fields.Char(string="Nombre de la etiqueta", required=True)
    employee_ids = fields.Many2many('sicpro.app.trabajadores.general',
                                    'sicpro_app_trabajadores_categorias_rel',
                                    'category_id', 'emp_id',
                                    string='Trabajadores')
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
            'trabajadores_etiquetas_incrementar')
        res = super(TrabajadoresEtiquetas, self).create(vals)
        return res
