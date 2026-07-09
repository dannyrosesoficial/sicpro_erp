# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models

PRIORIDADES_ACTIVAS = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'), ('3', 'Muy Alta'), ]


class RepositorioInstitucionalEstados(models.Model):
    _name = "sicpro.app.repo.estados"
    _description = "Estado de los repositorios"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char(string='Nombre del estado', required=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    is_inicial = fields.Boolean(string='¿Etapa inicial?')
    is_revision = fields.Boolean(string='¿Etapa en Revisión?')
    is_won = fields.Boolean(string='¿Etapa publicada?')
    is_cancelado = fields.Boolean(string='¿Etapa Cancelada?')
    requirements = fields.Text(string='Requerimientos')
    fold = fields.Boolean(string='Replegado en la vista Kanban')
