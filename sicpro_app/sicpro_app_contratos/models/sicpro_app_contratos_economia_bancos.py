# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api, _
from odoo.exceptions import UserError


def _default_color():
    return randint(1, 11)


class ContratosBancos(models.Model):
    _name = 'sicpro.app.contratos.economia.bancos'
    _description = 'Bancos de los contratos'

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo \
            as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.\
                NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string='Nombre', required=True)
    tipo_banco = fields.Selection(string='Tipo de Banco',
                                  selection=[('dvpe', 'Banco DVPE'), (
                                      'beneficiario', 'Banco Beneficiario'), ],
                                  required=True, default='dvpe')
    filtro_banco = fields.Selection(string='Filtro de Banco',
        selection=[('bfi', 'BFI'), ('metropolitano', 'Metropolitano'), ],
        required=False, default='bfi')
    calle = fields.Char(string='Calle', required=True)
    calle2 = fields.Char(string='Calle 2')
    postal = fields.Char(string='C.P.')
    municipios_id = fields.Many2one(comodel_name='res.municipality',
                                string='Municipio', required=False,
                                domain="[('state_id', '=', provincia_id)]")
    provincia_id = fields.Many2one(comodel_name='res.country.state',
                                   string='Provincia', required=False, )
    correo = fields.Char(string='Correo electrónico')
    telefono = fields.Char(string='Teléfono')
    active = fields.Boolean(default=True)
    codigo_id_bancaria = fields.Char(string='Sucursal Bancaria', index=True,
                                     required=True)
    swift = fields.Char(string='Swift', required=False)
    cuenta_dvpe = fields.Many2many(
        'sicpro.app.contratos.economia.cuentas.dvpe',
        'sicpro_app_contratos_cuentas_dvpe_rel', string='Nombre Cuenta DVPE',
        required=False)
    cuenta_beneficiario = fields.Many2many(
        'sicpro.app.contratos.beneficiarios',
        'sicpro_app_contratos_beneficiarios_rel',
        string='Nombre Cuenta Beneficiario', required=False)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

