# -*- coding: utf-8 -*-

from odoo import models, fields


class NomencladorEmplazamientos(models.Model):
    _name = 'sicpro.nomenclador.emplazamientos'
    _description = 'Nomenclador de Emplazamientos'

    name = fields.Char('Emplazamiento', required=True)
    centro_planificacion = fields.Many2one(string='Centro Planificación', required=True,
                                           comodel_name='sicpro.nomenclador.centro.planificacion', )
    active = fields.Boolean(string="Activo", default=True, )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El Centro de costo ya existe !"),
    ]
