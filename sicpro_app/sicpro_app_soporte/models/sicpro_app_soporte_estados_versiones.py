# -*- coding: utf-8 -*-

from odoo import fields, models


class SoporteEstadosVersiones(models.Model):
    _name = 'sicpro.app.soporte.estados.versiones'
    _description = 'Estados de las versiones del sistema'
    _order = 'sequence, id'

    name = fields.Char(string='Estado', required=True)
    descripcion = fields.Text(string='Descripción')
    sequence = fields.Integer(default=1)
    active = fields.Boolean(default=True)
    inicial = fields.Boolean(string='Estado Desarrollo')
    closed = fields.Boolean(string='Estado Final')
    fold = fields.Boolean(string='Solapado en Kanban')
