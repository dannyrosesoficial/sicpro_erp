# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NomencladorCentroCosto(models.Model):
    _name = 'sicpro.nomenclador.centro.costo'
    _description = 'Nomenclador de Centros de Costos'

    name = fields.Char('Centro Costo', required=True)
    descripcion = fields.Char('Descripción', required=False)
    company_id = fields.Many2one(comodel_name="res.company", string="Proceso",
                                 required=True, )
    active = fields.Boolean(string="Activo", default=True, )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El Centro de costo ya existe !"),
    ]
