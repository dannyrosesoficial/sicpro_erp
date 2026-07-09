# -*- coding: utf-8 -*-

import time

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class OrdenesTrabajo(models.Model):
    _inherit = 'sicpro.app.ordenes.trabajo'

    saldo_restante = fields.Monetary(string='Saldo Restante', currency_field='company_currency',
                                     compute='_compute_saldo_restante_as', store=False)
    saldo_contabilizado = fields.Monetary(string='Saldo Contabilizado', currency_field='company_currency',
                                          compute='_compute_saldo_restante_as', store=False)
    saldo_pendiente_contabilizar = fields.Monetary(string='Saldo Pendiente', currency_field='company_currency',
                                                   compute='_compute_saldo_pendiente', store=False)
    saldo_negativo = fields.Boolean(string='Saldo_negativo', default=False)

    # buscar el valor total contabilizado de la orden de trabajo
    def _compute_saldo_restante_as(self):
        valor_contabilizado = 0.0
        for item in self:
            contabilizado = self.env['sicpro.app.transferencias.gastos.ordenes'].search(
                ['&', ('terminado', '=', True), ('name', '=', item.id)])

            for data in contabilizado:
                valor_contabilizado += data.total_gastos

            if contabilizado:
                item.saldo_contabilizado = valor_contabilizado
                if item.as_valor:
                    item.saldo_restante = item.as_valor - valor_contabilizado
                    # verifico si existe saldo negativo
                    if item.saldo_restante < 0:
                        item.saldo_negativo = True
                    else:
                        item.saldo_negativo = False
                else:
                    item.saldo_restante = 0
            else:
                item.saldo_contabilizado = 0
                item.saldo_restante = 0

    # buscar el valor total pendiente por contabilizar de la orden de trabajo
    def _compute_saldo_pendiente(self):
        valor_por_contabilizado = 0.0
        for item in self:
            por_contabilizar = self.env['sicpro.app.transferencias.gastos.ordenes'].search(
                ['&', ('terminado', '!=', True), ('name', '=', item.id)])

            for data in por_contabilizar:
                valor_por_contabilizado += data.total_gastos

            if por_contabilizar:
                item.saldo_pendiente_contabilizar = valor_por_contabilizado
            else:
                item.saldo_pendiente_contabilizar = 0

    # ver saldo contabilizado de la orden de trabajo
    def ver_saldo_contabilizado(self):
        self.ensure_one()
        domain = ['&', ('terminado', '=', True), ('name', '=', self.id)]
        return {
            'name': _('Certificación de Gastos Contabilizados'),
            'domain': domain,
            'res_model': 'sicpro.app.transferencias.gastos.ordenes',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'limit': 80,
            'context': "{'search_default_anio': %s}" % time.strftime('%Y')
        }

    # ver saldo contabilizado de la orden de trabajo
    def ver_saldo_pendiente_contabilizar(self):
        self.ensure_one()
        domain = ['&', ('terminado', '!=', True), ('name', '=', self.id)]
        return {
            'name': _('Certificación de Gastos Pendientes por Contabilizar'),
            'domain': domain,
            'res_model': 'sicpro.app.transferencias.gastos.ordenes',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'limit': 80,
            'context': "{'search_default_anio': %s}" % time.strftime('%Y')
        }

    # ver saldo contabilizado de la orden de trabajo
    def ver_saldo_restante(self):
        if self.saldo_restante != 0:
            view = self.env.ref('sicpro_app_transferencias_gastos.ordenes_trabajo_control_gastos_tree')
            self.ensure_one()
            domain = [('id', '=', self.id)]
            return {
                'name': _('Control de Gastos de Órdenes de Trabajo'),
                'domain': domain,
                'res_model': 'sicpro.app.ordenes.trabajo',
                'type': 'ir.actions.act_window',
                'view_id':  view.id,
                'view_mode': 'tree',
                'limit': 80,
            }
        else:
            raise ValidationError(_("¡No se encuentran valores de gastos pendientes en la Orden de Trabajo!. "
                                    "Si cree que es un error contacte al administrador"))


