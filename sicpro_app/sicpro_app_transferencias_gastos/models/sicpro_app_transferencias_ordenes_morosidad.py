# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class TransferenciasGastosOrdenesMorosidad(models.Model):
    _name = "sicpro.app.transferencias.gastos.ordenes.morosidad"
    _description = "Periodo de tiempo en que se debe recibir la certificación de gastos"
    _order = "sequence asc"

    name = fields.Integer('Periodo (días)', required=True)
    sequence = fields.Integer('Secuencia', default=1, )
    active = fields.Boolean('Activo', default=True)
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor', domain="[('ejecuta_proceso', '=', True)]",
                                 required=True, default=lambda self: self.env.company)
    company_abreviatura = fields.Char(string='Abreviatura', required=False, related='company_id.identificador_corto')
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    _sql_constraints = [
        ('name_uniq', 'unique (company_id)', "¡El nombre del proceso ya existe!"),
    ]