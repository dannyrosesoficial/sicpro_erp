# -*- coding: utf-8 -*-

from odoo import fields, models

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class SolicitudesEstados(models.Model):
    _name = "sicpro.app.solicitudes.estados"
    _description = "Estado de Solicitudes"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Nombre del estado', required=True, translate=True)
    sequence = fields.Integer('Secuencia', default=1,)
    is_inicial = fields.Boolean('¿Es la Etapa inicial?')
    is_won = fields.Boolean('¿Es la Etapa Ganada?')
    requirements = fields.Text('Requerimientos',
                               help="Enter here the internal requirements for this stage (ex: Offer "
                                    "sent to customer). It will appear as a tooltip over the "
                                                      "stage's name.")
    fold = fields.Boolean('Replegado en la vista Kanban',)
