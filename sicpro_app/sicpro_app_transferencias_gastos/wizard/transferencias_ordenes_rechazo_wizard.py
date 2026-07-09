# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import fields, models
from odoo.tools import format_date


class TransferenciasOrdenesRechazo(models.TransientModel):
    _name = 'sicpro.app.transferencias.ordenes.rechazadas.wizard'
    _description = 'Motivo de rechazo de los gastos de las transferencias'

    motivo_id = fields.Text(string="Motivo de Rechazo", required=True)

    def action_motivo_rechazo(self):
        gastos = self.env['sicpro.app.transferencias.gastos.ordenes'].browse(self.env.context.get('active_ids'))
        if gastos.rol_interno == 'dtp':
            estado = self.env['sicpro.app.transferencias.gastos.ordenes.estados'].search(
                [('color_barra', '=', 'danger'), ('rol_interno', '=', 'economia')])
            for item in gastos:
                item.certificacion_rechazada = True
                item.fecha_rechazada = datetime.today()
                item.estado_id = estado.id
                item.motivo_rechazo = 'Los gastos fueron rechazados él ' + str(
                    format_date(self.env, datetime.today())) + ' por los siguientes motivos: ' + str(self.motivo_id)
                # actualizo el estado de los gastos de la cj74
                estado_gastos = estado.valor_tecnico_gastos
                for value in item.gastos_ids:
                    value.sudo().estado = estado_gastos
                    value.sudo().motivo_rechazo = self.motivo_id

                # Selecciono el registro de seguidores de economía
                group_eco = self.env.ref('sicpro_app_transferencias_gastos.grupo_transferencias_economia').users
                for participante in group_eco:
                    # envío el correo electrónico
                    email_values = {'email_to': participante.email_formatted, }
                    local_context = self.env.context.copy()
                    template = self.env.ref('sicpro_app_transferencias_gastos.gastos_rechazo_orden_dtp')
                    template.with_context(local_context).send_mail(item.id, force_send=True, email_values=email_values)

        elif gastos.rol_interno == 'ejecutores':
            estado = self.env['sicpro.app.transferencias.gastos.ordenes.estados'].search(
                [('color_barra', '=', 'warning'), ('rol_interno', '=', 'dtp')])
            for item in gastos:
                item.certificacion_rechazada = True
                item.fecha_rechazada = datetime.today()
                item.estado_id = estado.id
                item.motivo_rechazo = 'Los gastos fueron rechazados él ' + str(
                    format_date(self.env, datetime.today())) + ' por los siguientes motivos: ' + str(self.motivo_id)
                # actualizo el estado de los gastos de la cj74
                estado_gastos = estado.valor_tecnico_gastos
                for value in item.gastos_ids:
                    value.sudo().estado = estado_gastos
                    value.sudo().motivo_rechazo = self.motivo_id

                # Selecciono el registro de seguidores DTP
                group_dtp = self.env.ref('sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos').users
                for participante in group_dtp:
                    if participante.company_id.identificador_corto == item.company_abreviatura:
                        # envío el correo electrónico
                        email_values = {'email_to': participante.email_formatted, }
                        local_context = self.env.context.copy()
                        template = self.env.ref('sicpro_app_transferencias_gastos.gastos_rechazo_orden_ejecutor')
                        template.with_context(local_context).send_mail(item.id, force_send=True, email_values=email_values)

        elif gastos.rol_interno == 'inversionistas':
            estado = self.env['sicpro.app.transferencias.gastos.ordenes.estados'].search(
                [('color_barra', '=', 'danger'), ('rol_interno', '=', 'ejecutores')])
            for item in gastos:
                item.certificacion_rechazada = True
                item.fecha_rechazada = datetime.today()
                item.estado_id = estado.id
                item.motivo_rechazo = 'Los gastos fueron rechazados él ' + str(
                    format_date(self.env, datetime.today())) + ' por los siguientes motivos: ' + str(self.motivo_id)
                # actualizo el estado de los gastos de la cj74
                estado_gastos = estado.valor_tecnico_gastos
                for value in item.gastos_ids:
                    value.sudo().estado = estado_gastos
                    value.sudo().motivo_rechazo = self.motivo_id

                # Selecciono el registro de seguidores ejecutores
                group_ejecutor = self.env.ref('sicpro_app_transferencias_gastos.grupo_transferencias_ejecutores_procesos').users
                for participante in group_ejecutor:
                    if participante.company_id.identificador_corto == item.company_abreviatura:
                        # envío el correo electrónico
                        email_values = {'email_to': participante.email_formatted, }
                        local_context = self.env.context.copy()
                        template = self.env.ref('sicpro_app_transferencias_gastos.gastos_rechazo_orden_inversionista')
                        template.with_context(local_context).send_mail(item.id, force_send=True, email_values=email_values)

        else:
            estado = self.env['sicpro.app.transferencias.gastos.ordenes.estados'].search(
                [('color_barra', '=', 'info'), ('rol_interno', '=', 'dtp')])
            for item in gastos:
                item.certificacion_rechazada = True
                item.fecha_rechazada = datetime.today()
                item.estado_id = estado.id
                item.certificacion_rechazada = False
                item.motivo_rechazo = 'Los gastos fueron rechazados él ' + str(
                    format_date(self.env, datetime.today())) + ' por los siguientes motivos: ' + str(self.motivo_id)
                # actualizo el estado de los gastos de la cj74
                estado_gastos = estado.valor_tecnico_gastos
                for value in item.gastos_ids:
                    value.sudo().estado = estado_gastos
                    value.sudo().motivo_rechazo = self.motivo_id

                # Selecciono el registro de seguidores del DTP
                group_dtp = self.env.ref('sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos').users
                for participante in group_dtp:
                    if participante.company_id.identificador_corto == item.company_abreviatura:
                        # envío el correo electrónico
                        email_values = {'email_to': participante.email_formatted, }
                        local_context = self.env.context.copy()
                        template = self.env.ref('sicpro_app_transferencias_gastos.gastos_rechazo_orden_economia')
                        template.with_context(local_context).send_mail(item.id, force_send=True, email_values=email_values)

        # redirecciono la salida
        action = \
            self.sudo().env.ref('sicpro_app_transferencias_gastos.transferencias_ordenes_gastos_action').read()[0]
        return action
