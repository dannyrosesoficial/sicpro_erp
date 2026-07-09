# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CategoriaOcupacional(models.Model):
    _name = 'sicpro.nomenclador.categoria.ocupacional'
    _description = 'Categoría Ocupacional de los Procesos'

    name = fields.Char(string='Categoría Ocupacional', required=True,
                       index=True,)
    descripcion = fields.Text(string='Descripción de la categoría')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    salario = fields.Monetary("Salario", currency_field='company_currency_id',
                              required=True)
    alimentacion = fields.Monetary("Alimentación", required=True,
                                   currency_field='company_currency_id')

    _sql_constraints = [
        ('name_company_uniq', 'unique(name)',
         'Ya existe esa categoría ocupacional en el proceso especifico'),
    ]
    active = fields.Boolean(string="Activo", default=True, )
