# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VariablesEstadisticas(models.Model):
    _name = 'sicpro.nomenclador.variables'
    _description = 'Nomenclador de Variables'

    name = fields.Selection(string='Variable', selection=[
        ('estimulacion', 'Estimulación'),
        ('vacaciones', 'Reserva de Vacaciones'),
        ('seguridad_social', 'Seguridad Social'),
        ('gastos_indirectos', 'Gastos Indirectos'),
        ('imprevisto', 'Actividades imprevistas'),
    ], required=True, )
    descripcion = fields.Char(string='Descripción', required=False)
    porciento = fields.Char(string="Valor %", required=True)
    valor = fields.Float(string='Valor', required=True)
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Proceso", required=True, )
    active = fields.Boolean(string="Activo", default=True, )

    _sql_constraints = [
        ('name_uniq', 'unique(name, company_id)',
         'Ya existe esa variable estadística en el proceso especifico'),
    ]
