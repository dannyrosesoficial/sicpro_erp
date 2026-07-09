# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api, _


def _default_color():
    return randint(1, 11)


class ContratosCuentasDVPE(models.Model):
    _name = 'sicpro.app.contratos.economia.cuentas.dvpe'
    _description = 'Registro de cuentas de la DVPE'

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo \
            as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.\
                NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string='Nombre', required=True)
    cuenta = fields.Char(string='Cuenta Bancaria', size=16, required=True)
    direccion = fields.Char(
        string='Dirección', required=True,
        default='Ave. Salvador Allende # 508 entre Calle Santiago y '
                'Belascoain, Centro Habana, La Habana, Cuba.')
    telefono = fields.Char(string='Teléfono', default='78741548',
                           required=True)
    moneda = fields.Many2one('res.currency', string='Moneda', required=True)
    color = fields.Integer(string='Color',
        default=lambda self: _default_color())
    active = fields.Boolean(default=True)
