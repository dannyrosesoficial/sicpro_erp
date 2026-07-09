# -*- coding: utf-8 -*-


from odoo import models, fields


class TransferenciasGastosAjustesHistorial(models.Model):
    _name = 'sicpro.app.transferencias.gastos.ajustes.historial'
    _order = "id desc"
    _description = 'Historial de Ajustes de Gastos de la CJ74'

    name = fields.Many2one(comodel_name='sicpro.app.ordenes.trabajo', string="Orden de Trabajo", required=False)
    anio = fields.Char(string='Año', required=False)
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses', string='Mes', required=False)
    cl_coste = fields.Char(string='Cl.coste', required=False)
    valor_var_anterior = fields.Monetary(currency_field='company_currency', string="Valor Anterior")
    valor_var_nuevo = fields.Monetary(currency_field='company_currency', string="Valor Nuevo")
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    company_currency = fields.Many2one("res.currency", string='Currency', related='company_id.currency_id', )
    company_abreviatura = fields.Char(string='Abreviatura', required=False, related='company_id.identificador_corto')
    cliente_id = fields.Many2one('sicpro.app.clientes', string='Cliente', related='name.cliente_id', required=True)


