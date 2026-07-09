# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TarifaHoraria(models.Model):
    _name = 'sicpro.nomenclador.tarifa.horaria'
    _description = 'Tarifa Horaria de los Procesos'

    name = fields.Float(required=True, string='Tarifa Horaria')
    descripcion = fields.Char(string="Descripción", )
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Proceso", required=True, )
    active = fields.Boolean(string="Activo", default=True, )
