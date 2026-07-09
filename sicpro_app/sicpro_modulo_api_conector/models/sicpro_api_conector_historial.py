# -*- coding: utf-8 -*-


from odoo import models, fields


class ApiConectorHistorial(models.Model):
    _name = 'sicpro.modulo.api.conector.historial'
    _order = "id desc"
    _description = 'Historial de conexiones con las apis externas'

    name = fields.Char(string="Aplicación", required=True, )
    app_externa = fields.Char('ID Aplicación', required=False)
    fecha_inicio = fields.Datetime(string='Inicio', required=False)
    fecha_fin = fields.Datetime(string='Fin', required=False)
    registros_creados = fields.Integer(string='Registros Creados', required=False)
    registros_actualizados = fields.Integer(string='Registros Actualizados', required=False)
    registros_archivados = fields.Integer(string='Registros Archivados', required=False)
    estado = fields.Selection(string='Estado', required=False, selection=[('exito', 'Éxito'), ('fallido', 'Fallido'), ])

