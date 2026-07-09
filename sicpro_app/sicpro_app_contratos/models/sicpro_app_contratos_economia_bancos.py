# -*- coding: utf-8 -*-

from random import randint
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ContratosBancos(models.Model):
    _name = 'sicpro.app.contratos.economia.bancos'
    _description = 'Bancos de los contratos'

    def _default_color(self):
        return randint(1, 11)

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
    municipio = fields.Many2one(comodel_name='sicpro.nomenclador.municipio',
                                string='Municipio', required=False,
                                domain="[('provincia', '=', provincia)]")
    provincia = fields.Many2one(comodel_name='sicpro.nomenclador.provincia',
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
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())

