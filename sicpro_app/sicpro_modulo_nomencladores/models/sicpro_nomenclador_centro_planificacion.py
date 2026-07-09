# -*- coding: utf-8 -*-

from odoo import models, fields


class NomencladorCentroPlanificacion(models.Model):
    _name = 'sicpro.nomenclador.centro.planificacion'
    _description = 'Nomenclador de Centros de Planificación (CePl)'

    name = fields.Char('CePl', required=True)    
    descripcion = fields.Char(string="Descripción", required=True, )
    active = fields.Boolean(string="Activo", default=True, )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El Centro de Planificación ya existe !"),
    ]
