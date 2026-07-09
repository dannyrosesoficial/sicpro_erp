# -*- coding: utf-8 -*-


from odoo import fields, models


class TransporteEstados(models.Model):
    _name = 'sicpro.app.transporte.estado'
    _order = 'sequence, id'
    _description = 'Estados del transporte'

    name = fields.Char(string="Nombre", required=True, )
    sequence = fields.Integer('Sequence', default=20)