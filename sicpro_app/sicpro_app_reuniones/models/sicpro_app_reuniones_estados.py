# -*- coding: utf-8 -*-

from odoo import _, fields, models


class ReunionesEstados(models.Model):
    _name = 'sicpro.app.reuniones.estados'
    _description = 'Estados de las Reuniones'
    _order = 'sequence, name'

    name = fields.Char(string='Nombre del estado', required=True)
    description = fields.Text(string='Descripción del estado')
    sequence = fields.Integer('Sequence', default=1)
    fold = fields.Boolean(string='Solapado en kanban', default=False)
    pipe_end = fields.Boolean(string='Estado final', default=False)
