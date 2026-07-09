# -*- coding: utf-8 -*-

from odoo import fields, models


class SoporteEstadospaquetes(models.Model):
    _name = 'sicpro.app.soporte.estados.paquetes'
    _description = 'Estados de los paquetes del sistema'
    _order = 'sequence, id'

    name = fields.Char(string='Estado', required=True)
    descripcion = fields.Text(string='Descripción')
    sequence = fields.Integer(default=1)
    active = fields.Boolean(default=True)
    inicial = fields.Boolean(string='Estado inicial')
    closed = fields.Boolean(string='Estado final')
    fold = fields.Boolean(string='Solapado en Kanban')
