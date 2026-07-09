# -*- coding: utf-8 -*-

from odoo import models, fields


class NomencladorAreasEmpresa(models.Model):
    _name = 'sicpro.nomenclador.areas.empresa'
    _description = 'Nomenclador de Área de Empresa'

    name = fields.Integer('Área de Empresa', required=True)
    descripcion = fields.Char(string="Descripción", required=True, )
    active = fields.Boolean(string="Activo", default=True, )

    _sql_constraints = [('name_uniq', 'unique (name)', "¡El Área de Empresa ya existe!"), ]
