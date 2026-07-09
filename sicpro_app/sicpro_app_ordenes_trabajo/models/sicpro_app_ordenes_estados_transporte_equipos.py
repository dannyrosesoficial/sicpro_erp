# -*- coding: utf-8 -*-

from odoo import fields, models

Prioridades_Activas = [
    ('0', 'Baja'),
    ('1', 'Media'),
    ('2', 'Alta'),
    ('3', 'Muy Alta'),
]


class OrdenesEstadosTransporteEquipos(models.Model):
    _name = "sicpro.app.ordenes.estados.transporte.equipos"
    _description = "Estado del transporte y los equipos en las obras"
    _rec_name = 'name'
    _order = "sequence asc"

    name = fields.Char('Nombre del estado', required=True)
    tipo = fields.Selection(
        string='Tipo',
        selection=[('vehiculo', 'Vehículos'), ('equipo_especializado', 'Equipos Especializados'),
                   ('equipo_complementario', 'Equipos Complementarios'), ], required=True, )
    sequence = fields.Integer('Secuencia', default=1,)
    detalles = fields.Text('Detalles')
    active = fields.Boolean('Activo', default=True)
    contar = fields.Boolean('Contar', default=False)
