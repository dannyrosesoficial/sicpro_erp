# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import time
from odoo import fields, models
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError

class OrdenesTrabajo(models.Model):
    _inherit = 'sicpro.app.ordenes.trabajo'

    # Campos unificados: store=True y compute_sudo=False para consistencia en Odoo 19
    saldo_restante = fields.Monetary(
        string='Saldo Restante',
        currency_field='company_currency',
        compute='_compute_saldo_restante_as',
        store=True,
        compute_sudo=False
    )
    saldo_contabilizado = fields.Monetary(
        string='Saldo Contabilizado',
        currency_field='company_currency',
        compute='_compute_saldo_restante_as',
        store=True,
        compute_sudo=False
    )
    saldo_pendiente_contabilizar = fields.Monetary(
        string='Saldo Pendiente',
        currency_field='company_currency',
        compute='_compute_saldo_pendiente',
        store=True,
        compute_sudo=False
    )
    saldo_negativo = fields.Boolean(
        string='Saldo_negativo',
        default=False,
        compute='_compute_saldo_restante_as',
        store=True,
        compute_sudo=False
    )

    # Buscar el valor total contabilizado de la orden de trabajo
    def _compute_saldo_restante_as(self):
        for item in self:
            item.saldo_contabilizado = 0.0
            item.saldo_restante = 0.0
            item.saldo_negativo = False

        if not self.ids:
            return

        # Uso de API Odoo 19: _read_group
        data = self.env['sicpro.app.transferencias.gastos.ordenes']._read_group(
            domain=[('terminado', '=', True), ('name', 'in', self.ids)],
            groupby=['name'],
            aggregates=['total_gastos:sum']
        )

        # Mapeamos los resultados: { orden_id: total_gastos }
        mapped_data = {name.id: total_gastos_sum for name, total_gastos_sum in data}

        for item in self:
            valor_contabilizado = mapped_data.get(item.id, 0.0)
            item.saldo_contabilizado = valor_contabilizado
            item.saldo_restante = (item.as_valor or 0.0) - valor_contabilizado
            item.saldo_negativo = item.saldo_restante < 0

    # Buscar el valor total pendiente por contabilizar de la orden de trabajo
    def _compute_saldo_pendiente(self):
        for item in self:
            item.saldo_pendiente_contabilizar = 0.0

        if not self.ids:
            return

        # Uso de API Odoo 19: _read_group
        data = self.env['sicpro.app.transferencias.gastos.ordenes']._read_group(
            domain=[('terminado', '!=', True), ('name', 'in', self.ids)],
            groupby=['name'],
            aggregates=['total_gastos:sum']
        )

        mapped_pending = {name.id: total_gastos_sum for name, total_gastos_sum in data}

        for item in self:
            item.saldo_pendiente_contabilizar = mapped_pending.get(item.id, 0.0)

    # Ver saldo contabilizado de la orden de trabajo
    def ver_saldo_contabilizado(self):
        self.ensure_one()
        domain = ['&', ('terminado', '=', True), ('name', '=', self.id)]
        return {
            'name': 'Certificación de Gastos Contabilizados',
            'domain': domain,
            'res_model': 'sicpro.app.transferencias.gastos.ordenes',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'limit': 80,
            'context': "{'search_default_anio': %s}" % time.strftime('%Y')
        }

    # Ver saldo pendiente de la orden de trabajo
    def ver_saldo_pendiente_contabilizar(self):
        self.ensure_one()
        domain = ['&', ('terminado', '!=', True), ('name', '=', self.id)]
        return {
            'name': 'Certificación de Gastos Pendientes por Contabilizar',
            'domain': domain,
            'res_model': 'sicpro.app.transferencias.gastos.ordenes',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'limit': 80,
            'context': "{'search_default_anio': %s}" % time.strftime('%Y')
        }

    # Ver control de gastos restante
    def ver_saldo_restante(self):
        if self.saldo_restante != 0:
            view = self.env.ref('sicpro_app_transferencias_gastos.ordenes_trabajo_control_gastos_list')
            self.ensure_one()
            domain = [('id', '=', self.id)]
            return {
                'name': 'Control de Gastos de Órdenes de Trabajo',
                'domain': domain,
                'res_model': 'sicpro.app.ordenes.trabajo',
                'type': 'ir.actions.act_window',
                'view_id': view.id,
                'view_mode': 'tree',
                'limit': 80,
            }
        else:
            raise ValidationError(
                "¡No se encuentran valores de gastos pendientes en la Orden de Trabajo!.\n\n" + MSG_SOPORTE_SICPRO)