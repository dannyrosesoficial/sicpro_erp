# -*- coding: utf-8 -*-

from odoo import fields, models

Prioridades_Activas = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'), ('3', 'Muy Alta'), ]


class RepositorioInstitucionalEstados(models.Model):
    _name = "sicpro.app.repo.estados"
    _description = "Estado de los repositorios"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Nombre del estado', required=True)
    sequence = fields.Integer('Secuencia', default=1, )
    is_inicial = fields.Boolean('¿Etapa inicial?')
    is_revision = fields.Boolean('¿Etapa en Revisión?')
    is_won = fields.Boolean('¿Etapa publicada?')
    is_cancelado = fields.Boolean('¿Etapa Cancelada?')
    requirements = fields.Text('Requerimientos')
    fold = fields.Boolean('Replegado en la vista Kanban', )
