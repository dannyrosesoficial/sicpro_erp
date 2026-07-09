# -*- coding: utf-8 -*-

from odoo import fields, models


class MetrologiaEstado(models.Model):
    _name = 'sicpro.app.metrologia.estado'
    _description = 'Estados del Mantenimiento'
    _order = 'sequence, id'

    name = fields.Char('Estado', required=True,)
    sequence = fields.Integer('Sequence', default=20)
    fold = fields.Boolean('Plegado en el flujo de mantenimiento')
    done = fields.Boolean('Solicitud hecha')
