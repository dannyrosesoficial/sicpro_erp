# -*- coding: utf-8 -*-

from odoo import fields, models

Prioridades_Activas = [
    ('0', 'Baja'),
    ('1', 'Media'),
    ('2', 'Alta'),
    ('3', 'Muy Alta'),
]


class ContratosProveedoresEstados(models.Model):
    _name = 'sicpro.app.contratos.proveedores.estados'
    _description = 'Estados del proveedor'
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Nombre del estado', required=True, translate=True)
    sequence = fields.Integer('Secuencia', default=1, )
    is_inicial = fields.Boolean('¿Es la Etapa inicial?')
    is_rechazada = fields.Boolean('¿Es la Etapa Rechazada?')
    is_aprobada = fields.Boolean('¿Es la Etapa de aprobación?')
    is_won = fields.Boolean('¿Es la Etapa Ganada?')
    is_final = fields.Boolean('¿Es la Etapa Final?')
    description = fields.Text('Requerimientos',
                               help="Enter here the internal requirements for this stage (ex: Offer "
                                    "sent to customer). It will appear as a tooltip over the "
                                    "stage's name.")
    fold = fields.Boolean('Replegado en la vista Kanban', )
