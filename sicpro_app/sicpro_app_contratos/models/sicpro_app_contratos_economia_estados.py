# -*- coding: utf-8 -*-

from odoo import fields, models

Prioridades_Activas = [
    ('0', 'Baja'),
    ('1', 'Media'),
    ('2', 'Alta'),
    ('3', 'Muy Alta'),
]


class ContratosEconomiaEstados(models.Model):
    _name = 'sicpro.app.contratos.economia.estados'
    _description = 'Estados económicos de los contratos'
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Nombre del estado', required=True, translate=True)
    sequence = fields.Integer('Secuencia', default=1, )
    is_inicial = fields.Boolean('¿Es la Etapa inicial?')
    is_instrumento = fields.Boolean('¿Es la Etapa de Solicitud del Instrumento?')
    is_emision = fields.Boolean('¿Es la Etapa de Emisión de Pago?')
    transito = fields.Boolean('¿Es la Etapa Aceptada o Entregado?')
    is_final = fields.Boolean('¿Es la Etapa Final?')
    description = fields.Text('Requerimientos')
    fold = fields.Boolean('Replegado en la vista Kanban', )
