# -*- coding: utf-8 -*-

from odoo import fields, models

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class ContratosEstados(models.Model):
    _name = 'sicpro.app.contratos.estados'
    _description = 'Estados de los contratos'
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Nombre del estado', required=True, translate=True)
    sequence = fields.Integer('Secuencia', default=1, )
    is_inicial = fields.Boolean('¿Es la Etapa inicial?')
    is_contratacion = fields.Boolean('¿Es la Etapa Contratación?')
    is_aprobada = fields.Boolean('¿Es la Etapa de aprobación?')
    is_legal = fields.Boolean('¿Es la Etapa Legal?')
    is_economia = fields.Boolean('¿Es la Etapa Económica?')
    is_economia_dc = fields.Boolean('¿Es la Etapa DC Economía?')
    is_firma_director = fields.Boolean('¿Es la Etapa Dirección?')
    is_firma_proveedor = fields.Boolean('¿Es la Etapa Proveedor?')
    is_rechazada = fields.Boolean('¿Es la Etapa Rechazada?')
    is_cancelada = fields.Boolean('¿Es la Etapa Cancelada?')
    is_terminada = fields.Boolean('¿Es la Etapa Terminada?')
    is_won = fields.Boolean('¿Es la Etapa Ganada?')
    description = fields.Text('Requerimientos',
                               help="Enter here the internal requirements for this stage (ex: Offer "
                                    "sent to customer). It will appear as a tooltip over the "
                                    "stage's name.")
    fold = fields.Boolean('Replegado en la vista Kanban', )
