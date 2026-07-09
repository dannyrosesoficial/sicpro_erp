# -*- coding: utf-8 -*-

from odoo import fields, models


class OrdenesProgramaInversiones(models.Model):
    _name = 'sicpro.app.ordenes.programa.inversiones'
    _description = 'Programa de Inversiones de las Órdenes de Trabajo'

    name = fields.Char('Descripción', required=True)
    plan = fields.Char(string='Plan', required=True)
    consecutivo = fields.Integer(string='Consecutivo', required=True)
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor', domain="[('ejecuta_proceso', '=', True)]",
                                 required=True, )
    company_abreviatura = fields.Char(string='Abreviatura', required=False, related='company_id.identificador_corto')
    active = fields.Boolean('Activo', default=True)
