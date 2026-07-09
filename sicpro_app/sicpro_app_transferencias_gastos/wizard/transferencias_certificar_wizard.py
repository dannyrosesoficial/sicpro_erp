# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.fields import Datetime
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from collections import defaultdict


class TransferenciasGastosCertificarWizard(models.TransientModel):
    _name = "sicpro.app.transferencias.gastos.economia.wizard"
    _description = "Enviar gastos a certificar"

    def _gastos_cj74_modificar_meses(self):
        gastos = self.env['sicpro.app.transferencias.gastos'].search(
            [('estado', '=', 'revision_economica')])
        if gastos:
            return gastos.mapped('mes').ids
        return []

    def _get_mes_domain(self):
        mes_ids = self._gastos_cj74_modificar_meses()
        return [('id', 'in', mes_ids)]

    anio = fields.Char(string="Año", required=True,
                       default=lambda self: Datetime.now().strftime("%Y"))
    mes_ids = fields.Many2many('sicpro.nomenclador.meses',
                               'transferencias_meses_rel', 'transferencia_id',
                               'mes_id', string='Meses', default=lambda
            self: self._gastos_cj74_modificar_meses(), domain=_get_mes_domain,
                               required=True)
    ordenes_ids = fields.Many2many('sicpro.app.ordenes.trabajo',
                                   'transferencias_ordenes_rel',
                                   'transferencia_id', 'ordenes_id',
                                   string='Ordenes', required=True)

    @api.onchange('mes_ids')
    def _compute_gastos_cj74_ordenes(self):
        if self.mes_ids:
            # Buscamos todas las órdenes de una sola vez (más eficiente)
            gastos = self.env['sicpro.app.transferencias.gastos'].search(
                [('estado', '=', 'revision_economica'),
                 ('mes', 'in', self.mes_ids.ids)])

            self.ordenes_ids = gastos.mapped('name')
        else:
            self.ordenes_ids = [(5, 0, 0)]

    def modificar_estado_gastos(self):
        if not self.mes_ids or not self.ordenes_ids:
            raise ValidationError(
                "Debe seleccionar meses y órdenes para certificar.\n\n" + MSG_SOPORTE_SICPRO)

        meses_ids = self.mes_ids
        ordenes_ids = self.ordenes_ids
        anio = self.anio
        anio_actual = Datetime.now().strftime("%Y")
        mes_actual_obj = self.env['sicpro.nomenclador.meses'].search(
            [("codigo_mes", "=", Datetime.now().strftime("%m"))], limit=1)
        mes_actual = mes_actual_obj.id if mes_actual_obj else False

        gastos_all = self.env['sicpro.app.transferencias.gastos'].search(
            [("anio", "=", anio), ("mes", "in", meses_ids.ids),
                ('estado', '=', 'revision_economica'),
                ("name", "in", ordenes_ids.ids)])

        # 2. Agrupamos los gastos en memoria usando un diccionario indexado por (mes_id, orden_id)
        gastos_agrupados = defaultdict(
            lambda: self.env['sicpro.app.transferencias.gastos'])
        for g in gastos_all:
            gastos_agrupados[(g.mes.id, g.name.id)] += g

        # 3. Iteramos las agrupaciones reales existentes reduciendo drásticamente las escrituras e inserciones
        for (mes_id, orden_id), b_gastos in gastos_agrupados.items():
            orden_transferencias = self.env[
                'sicpro.app.transferencias.gastos.ordenes'].sudo().create(
                {'orden_id': orden_id, 'anio': anio_actual, 'mes': mes_actual,
                    'company_id': self.env.company.id,
                    # Consistencia garantizada para el multi-company (reglas ir.rule)
                })

            # Escritura masiva en lote para todos los gastos del grupo específico
            b_gastos.write({'gasto_id': orden_transferencias.id,
                'estado': 'revision_dtp'})

            # Disparador del campo computado
            _ = orden_transferencias.cantidad_cuentas
        try:
            grup_dtp = self.env.ref(
                'sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos',
                raise_if_not_found=False)
            group_dtp = self.env['res.users']
            if grup_dtp:
                group_dtp = grup_dtp.user_ids

            id_gastos = self.env['sicpro.app.transferencias.gastos'].search(
                [('active', '=', True)], limit=1)
            template = self.env.ref(
                'sicpro_app_transferencias_gastos.gastos_revision_economica_dtp')

            for participante in group_dtp:
                if participante.email_formatted:
                    template.send_mail(id_gastos.id, force_send=False,
                        email_values={'email_to': participante.email_formatted,
                            'email_from': '"SICPRO ERP" <sicproerp@etecsa.cu>', })
        except Exception:
            pass
        action_url = self.sudo().env.ref(
            'sicpro_app_transferencias_gastos.transferencias_gastos_action').read()[
            0]

        return {'type': 'ir.actions.client', 'tag': 'display_notification',
                'params': {'title': 'Éxito',
                           'message': 'Se realizó correctamente la transferencia de gastos.',
                           'sticky': False, 'type': 'success', 'next': action_url,}}