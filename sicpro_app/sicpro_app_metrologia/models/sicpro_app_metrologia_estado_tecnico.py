# -*- coding: utf-8 -*-

from odoo import fields, models


class MetrologiaEstadoTecnico(models.Model):
    _name = 'sicpro.app.metrologia.estado.tecnico'
    _description = 'Estado Técnico'

    name = fields.Char(string="Estado Técnico", required=True, )
    active = fields.Boolean(string="Activo", default=True, )
