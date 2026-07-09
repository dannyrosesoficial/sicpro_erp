# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ContratosDias(models.Model):
    _name = 'sicpro.app.contratos.dias'
    _description = 'Días hábiles para los contratos'

    name = fields.Selection(string='Variable', selection=[
        ('solicitante', 'Dias Solicitante'),
        ('contratacion', 'Días Comité de Contratación'),
        ('revision', 'Dias Revisión'),
        ('legal', 'Dias Legal'),
        ('economia', 'Dias Economía'),
        ('economia_dc', 'Dias Economía DC'),
        ('director_central', 'Dias Director'),
        ('proveedor', 'Dias Proveedor'),
        ('devolucion', 'Dias Devolución'),
    ], required=True, )

    descripcion = fields.Char(string='Descripción', required=False)
    valor = fields.Integer(string='Dias', required=True)
    # company_id = fields.Many2one(comodel_name="res.company",
    # string="Proceso", required=True, )
    active = fields.Boolean(string="Activo", default=True, )

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Ya existe la variable específica'), ]
