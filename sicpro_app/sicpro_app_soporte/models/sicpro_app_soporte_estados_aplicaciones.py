# -*- coding: utf-8 -*-

from odoo import fields, models


class SoporteEstadosAplicaciones(models.Model):
    _name = 'sicpro.app.soporte.estados.aplicaciones'
    _description = 'Estados de las aplicaciones del sistema'
    _order = 'sequence, id'

    name = fields.Char(string='Estado', required=True, translate=True)
    descripcion = fields.Text(string='Descripción')
    sequence = fields.Integer(default=1)
    active = fields.Boolean(default=True)
    inicial = fields.Boolean(string='Estado inicial')
    closed = fields.Boolean(string='Estado final')
    fold = fields.Boolean(string='Solapado en Kanban')
