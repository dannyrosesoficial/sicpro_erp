# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api


def _default_color():
    return randint(1, 11)


class ContratosBeneficiarios(models.Model):
    _name = 'sicpro.app.contratos.beneficiarios'
    _description = 'Beneficiarios de los contratos'
    _order = "sequence, name, id"

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo \
            as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.\
                NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char('Nombre del Beneficiario', required=True,)
    cuenta_beneficiario = fields.Char('Cuenta del Beneficiario', size=16,
                                      required=False,)
    moneda = fields.Many2one('res.currency', string='Moneda', required=False)
    sequence = fields.Integer('Secuencia', default=1, )
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
