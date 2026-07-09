# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api


class ContratosBeneficiarios(models.Model):
    _name = 'sicpro.app.contratos.beneficiarios'
    _description = 'Beneficiarios de los contratos'
    _order = "sequence, name, id"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char('Nombre del Beneficiario', required=True,)
    cuenta_beneficiario = fields.Char('Cuenta del Beneficiario', size=16,
                                      required=False,)
    moneda = fields.Many2one('res.currency', string='Moneda', required=False)
    sequence = fields.Integer('Secuencia', default=1, )
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())
