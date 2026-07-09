# -*- coding: utf-8 -*-

from odoo import fields, models


class MetrologiaEstadoTecnico(models.Model):
    _name = 'sicpro.app.metrologia.estado.tecnico'
    _description = 'Estado Técnico Metrología'

    name = fields.Char(string="Estado Técnico", required=True, )
    active = fields.Boolean(string="Activo", default=True, )
    sequence = fields.Integer('Sequence', default=20)
    fold = fields.Boolean('Plegado')
    laboratorio = fields.Boolean('En Laboratorio')
    sin_calibrar = fields.Boolean('Sin Calibrar')
    baja = fields.Boolean('Baja')
