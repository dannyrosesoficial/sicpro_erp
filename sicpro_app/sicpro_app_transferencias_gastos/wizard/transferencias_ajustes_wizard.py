# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo import fields, models
from odoo.exceptions import ValidationError


class TransferenciasGastosAjustes(models.TransientModel):
    _name = "sicpro.app.transferencias.gastos.ajustes"
    _description = "Ajustar valores de gastos"

    def _gasto_sap(self):
        gastos_id = None
        gastos = self.env.context.get(
            'active_model') == 'sicpro.app.transferencias.gastos' and self.env.context.get(
            'active_ids') or []

        gastos_browse = self.env['sicpro.app.transferencias.gastos'].browse(
            gastos)
        if not gastos_browse:
            return False
        gastos_id = gastos_browse[0]

        if gastos_id.contabilizado:
            raise ValidationError(
                "¡No se puede ajustar gastos de cuentas contabilizadas!.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            return gastos_id.id

    transferencia_sap = fields.Many2one(
        comodel_name='sicpro.app.transferencias.gastos',
        string='Transferencia sap', required=True, default=_gasto_sap)
    gasto_sap_anterior = fields.Monetary(currency_field='company_currency',
                                         string='Valor Anterior',
                                         required=True,
                                         related='transferencia_sap.valor_var')
    gasto_sap_nuevo = fields.Monetary(currency_field='company_currency',
                                      string='Nuevo Valor', required=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one("res.currency", string='Moneda',
                                       related='company_id.currency_id')

    # modifico gasto de la cj74 y agrego al historial
    def modificar_gasto_transferido(self):
        nuevo = self.gasto_sap_nuevo
        anterior = self.gasto_sap_anterior
        id_gasto = self.transferencia_sap.id
        cl_coste = self.transferencia_sap.cl_coste
        mes = self.transferencia_sap.mes.id
        anio = self.transferencia_sap.anio
        orden = self.transferencia_sap.name.id
        self.transferencia_sap.write({"valor_var": nuevo})

        self.env[
            'sicpro.app.transferencias.gastos.ajustes.historial'].sudo().create(
            {'name': orden, 'anio': anio, 'mes': mes, 'cl_coste': cl_coste,
                'valor_var_anterior': anterior, 'valor_var_nuevo': nuevo,
                'company_id': self.company_id.id, })