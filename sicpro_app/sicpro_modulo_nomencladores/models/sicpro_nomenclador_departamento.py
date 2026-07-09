# -*- coding: utf-8 -*-

from odoo import models, fields


class NomencladorDepartamentos(models.Model):
    _name = 'sicpro.nomenclador.departamentos'
    _description = 'Nomenclador Departamentos del Proceso'
    _order = 'sequence, id'

    name = fields.Char(required=True, string='Departamento')
    company_id = fields.Many2one(comodel_name="res.company", string="Proceso", required=True, )
    sequence = fields.Integer(default=1)
    active = fields.Boolean(string="Activo", default=True, )

    _sql_constraints = [('name_uniq', 'unique(name, company_id)',
                         'Ya existe el departamento en el proceso especifico'),
                        ]
