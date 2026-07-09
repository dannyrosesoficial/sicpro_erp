# -*- coding: utf-8 -*-

from odoo import fields, models


class OrdenesProgramaConsecutivos(models.Model):
    _name = 'sicpro.app.ordenes.consecutivos'
    _description = 'Programa de Inversiones de las Órdenes de Trabajo'

    name = fields.Char('nomenclador', required=True)
    moneda = fields.Char(string='Moneda', required=True)
    tipo = fields.Selection(string='Tipo de Orden',
                            selection=[('inversiones', 'Inversiones'), ('mantenimiento', 'Mantenimiento'), ],
                            required=True, )
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor', domain="[('ejecuta_proceso', '=', True)]",
                                 required=True, )
    company_abreviatura = fields.Char(string='Abreviatura', required=False, related='company_id.identificador_corto')
    active = fields.Boolean('Activo', default=True)
