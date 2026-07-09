# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TrabajadoresCargos(models.Model):
    _name = 'sicpro.app.trabajadores.cargos'
    _description = 'Cargos del Trabajador'

    name = fields.Char(string='Cargo del Trabajador', required=True,
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
    active = fields.Boolean(string="Activo", default=True, )

    _sql_constraints = [
        ('name_company_uniq', 'unique(name)',
         'Ya existe el cargo del trabajador'),
    ]