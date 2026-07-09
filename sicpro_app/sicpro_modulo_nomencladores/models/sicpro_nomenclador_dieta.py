# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EstadosDieta(models.Model):
    _name = 'sicpro.nomenclador.dieta'
    _description = 'Nomenclador de Dieta'

    name = fields.Float(required=True, string='Dieta')
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Proceso", required=True, )
    active = fields.Boolean(string="Activo", default=True, )

    _sql_constraints = [
        ('name_uniq', 'unique (company_id)',
         "La dieta del proceso seleccionado ya existe !"),
    ]
