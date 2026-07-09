# -*- coding: utf-8 -*-

from odoo import fields, models

Prioridades_Activas = [
    ('0', 'Baja'),
    ('1', 'Media'),
    ('2', 'Alta'),
    ('3', 'Muy Alta'),
]


class SolicitudesEstados(models.Model):
    _name = "sicpro.app.solicitudes.estados"
    _description = "Estado de Solicitudes"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Nombre del estado', required=True)
    sequence = fields.Integer('Secuencia', default=1,)
    is_inicial = fields.Boolean('¿Etapa inicial?')
    is_won = fields.Boolean('¿Etapa Ganada?')
    is_detenido = fields.Boolean('¿Etapa Detenida?')
    is_cancelado = fields.Boolean('¿Etapa Cancelada?')
    is_orden = fields.Boolean('¿Etapa vinculada a la OT?')
    requirements = fields.Text('Requerimientos')
    fold = fields.Boolean('Replegado en la vista Kanban',)
