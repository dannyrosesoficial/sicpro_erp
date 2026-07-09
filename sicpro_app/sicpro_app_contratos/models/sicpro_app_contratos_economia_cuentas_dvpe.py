# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api, _


class ContratosCuentasDVPE(models.Model):
    _name = 'sicpro.app.contratos.economia.cuentas.dvpe'
    _description = 'Registro de cuentas de la DVPE'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Nombre', required=True)
    cuenta = fields.Char(string='Cuenta Bancaria', size=16, required=True)
    direccion = fields.Char(
        string='Dirección', required=True,
        default='Ave. Salvador Allende # 508 entre Calle Santiago y '
                'Belascoain, Centro Habana, La Habana, Cuba.')
    telefono = fields.Char(string='Teléfono', default='78741548',
                           required=True)
    moneda = fields.Many2one('res.currency', string='Moneda', required=True)
    color = fields.Integer(string='Color Index',
        default=lambda self: self._default_color())
    active = fields.Boolean(default=True)
