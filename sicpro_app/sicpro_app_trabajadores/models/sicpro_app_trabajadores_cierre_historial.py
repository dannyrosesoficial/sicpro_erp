# -*- coding: utf-8 -*-

from odoo import models, fields


class TrabajadoresCierreHistorial(models.Model):
    _name = 'sicpro.app.trabajadores.cierre.historial'
    _description = "Historial de los cierres mensuales de Capital Humano"
    _order = "codigo_mes desc, name asc"

    name = fields.Selection(string='Estado', default='activo',
                            selection=[('activo', 'Activo'), ('archivado', 'Archivado'), ], )
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses', string='Mes', )
    codigo_mes = fields.Integer(string="Código Mes", related='mes.codigo_mes')
    anio = fields.Char(string='Año', default=fields.Datetime.now().strftime("%Y"))
    total = fields.Integer('Total de trabajadores', )
    altas = fields.Integer('Cantidad de altas', )
    bajas = fields.Integer('Cantidad de bajas', )
    usuario = fields.Many2one('res.users', string='Usuario')
    active = fields.Boolean('Activo', default=True)
