# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class TransferenciasGastosAjustes(models.TransientModel):
    _name = "sicpro.app.transferencias.gastos.ajustes"
    _description = "Ajustar valores de gastos"

    def _gasto_sap(self):
        gastos_id = None
        gastos = self._context.get('active_model') == 'sicpro.app.transferencias.gastos' and self._context.get(
            'active_ids') or []
        for item in self.env['sicpro.app.transferencias.gastos'].browse(gastos):
            gastos_id = item
        if gastos_id.contabilizado:
            raise ValidationError(_("¡No se puede ajustar gastos de cuentas contabilizadas!. "
                                    "Si cree que es un error contacte al administrador"))
        else:
            return gastos_id.id

    transferencia_sap = fields.Many2one(comodel_name='sicpro.app.transferencias.gastos', string='Transferencia sap',
                                        required=True, default=_gasto_sap)
    gasto_sap_anterior = fields.Monetary(currency_field='company_currency', string='Valor Anterior', required=True,
                                         related='transferencia_sap.valor_var')
    gasto_sap_nuevo = fields.Monetary(currency_field='company_currency', string='Nuevo Valor', required=True)
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    company_currency = fields.Many2one("res.currency", string='Currency', related='company_id.currency_id', )

    # modifico gasto de la cj74 y agrego al historial
    def modificar_gasto_transferido(self):
        nuevo = self.gasto_sap_nuevo
        anterior = self.gasto_sap_anterior
        id_gasto = self.transferencia_sap.id
        cl_coste = self.transferencia_sap.cl_coste
        mes = self.transferencia_sap.mes.id
        anio = self.transferencia_sap.anio
        orden = self.transferencia_sap.name.id
        gastos_sap = self.env['sicpro.app.transferencias.gastos'].search([('id', '=', id_gasto)])
        gastos_sap.write({"valor_var": nuevo})
        # agrego datos al historial de ajustes de gastos
        self.env['sicpro.app.transferencias.gastos.ajustes.historial'].sudo().create(
            {'name': orden, 'anio': anio, 'mes': mes, 'cl_coste': cl_coste, 'valor_var_anterior': anterior,
             'valor_var_nuevo': nuevo, })
