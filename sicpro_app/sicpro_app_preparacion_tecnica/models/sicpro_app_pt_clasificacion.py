# -*- coding: utf-8 -*-

from odoo import fields, models


class PreparacionTecnicaClasificacion(models.Model):
    _name = "sicpro.app.preparacion.tecnica.clasificacion"
    _description = "Clasificación de las actividades de la Preparación Técnica"

    name = fields.Char('Clasificación', required=True)
    especialidad = fields.Many2one("sicpro.nomenclador.especialidad",
                                   string="Especialidad", required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la clasificación existe!"),
    ]
