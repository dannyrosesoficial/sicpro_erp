# -*- coding: utf-8 -*-

from odoo import fields, models

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class PreparacionTecnicaEstados(models.Model):
    _name = 'sicpro.app.preparacion.tecnica.estados'
    _description = 'Estados de la Preparación Técnica'
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Nombre del estado', required=True, translate=True)
    sequence = fields.Integer('Secuencia', default=1, )
    is_inicial = fields.Boolean('¿Es la Etapa inicial?')
    is_won = fields.Boolean('¿Es la Etapa Ganada?')
    is_rechazada = fields.Boolean('¿Es la Etapa Rechazada?')
    is_aprobada = fields.Boolean('¿Es la Etapa de aprobación?')
    description = fields.Text('Requerimientos',
                               help="Enter here the internal requirements for this stage (ex: Offer "
                                    "sent to customer). It will appear as a tooltip over the "
                                    "stage's name.")
    fold = fields.Boolean('Replegado en la vista Kanban', )
