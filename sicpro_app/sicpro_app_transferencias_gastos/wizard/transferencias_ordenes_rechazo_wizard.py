# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
from datetime import datetime

from odoo import fields, models
from odoo.tools import format_date


class TransferenciasOrdenesRechazo(models.TransientModel):
    _name = 'sicpro.app.transferencias.ordenes.rechazadas.wizard'
    _description = 'Motivo de rechazo de los gastos de las transferencias'

    motivo_id = fields.Text(string="Motivo de Rechazo", required=True)

    def action_motivo_rechazo(self):
        gastos = self.env['sicpro.app.transferencias.gastos.ordenes'].browse(
            self.env.context.get('active_ids'))

        # 1. Definición de parámetros dinámicos según el rol del flujo interno
        rol = gastos.rol_interno
        domain_estado = []
        xml_grupo = ''
        xml_template = ''
        requiere_filtro_compania = True

        if rol == 'dtp':
            domain_estado = [('color_barra', '=', 'danger'),
                             ('rol_interno', '=', 'economia')]
            xml_grupo = 'sicpro_app_transferencias_gastos.grupo_transferencias_economia'
            xml_template = 'sicpro_app_transferencias_gastos.gastos_rechazo_orden_dtp'
            requiere_filtro_compania = False
        elif rol == 'ejecutores':
            domain_estado = [('color_barra', '=', 'warning'),
                             ('rol_interno', '=', 'dtp')]
            # Corrección del bug: Se apunta correctamente al grupo DTP de procesos y no al de economía
            xml_grupo = 'sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos'
            xml_template = 'sicpro_app_transferencias_gastos.gastos_rechazo_orden_ejecutor'
        elif rol == 'inversionistas':
            domain_estado = [('color_barra', '=', 'danger'),
                             ('rol_interno', '=', 'ejecutores')]
            xml_grupo = 'sicpro_app_transferencias_gastos.grupo_transferencias_ejecutores_procesos'
            xml_template = 'sicpro_app_transferencias_gastos.gastos_rechazo_orden_inversionista'
        else:
            domain_estado = [('color_barra', '=', 'info'),
                             ('rol_interno', '=', 'dtp')]
            xml_grupo = 'sicpro_app_transferencias_gastos.grupo_transferencias_dtp_procesos'
            xml_template = 'sicpro_app_transferencias_gastos.gastos_rechazo_orden_economia'

        # 2. Búsquedas y cargas de registros en base de datos ejecutadas una sola vez (Fuera de bucles)
        estado = self.env[
            'sicpro.app.transferencias.gastos.ordenes.estados'].search(
            domain_estado, limit=1)
        estado_gastos = estado.valor_tecnico_gastos if estado else False

        grup_obj = self.env.ref(xml_grupo, raise_if_not_found=False)
        group_users = grup_obj.user_ids if grup_obj else self.env['res.users']
        template = self.env.ref(xml_template, raise_if_not_found=False)

        fecha_texto = str(format_date(self.env, datetime.today()))
        motivo_formateado = f"Los gastos fueron rechazados él {fecha_texto} por los siguientes motivos: {str(self.motivo_id)}"

        # 3. Procesamiento en lote de los registros seleccionados
        for item in gastos:
            # Actualización directa sobre el registro de la orden rechazada
            item.write({'certificacion_rechazada': False if rol not in ['dtp',
                                                                        'ejecutores',
                                                                        'inversionistas'] else True,
                'fecha_rechazada': datetime.today(),
                'estado_id': estado.id if estado else False,
                'motivo_rechazo': motivo_formateado})

            # Optimización masiva de las sub-cuentas vinculadas (Evita bucles SQL redundantes)
            if item.gastos_ids:
                item.gastos_ids.sudo().write({'estado': estado_gastos,
                    'motivo_rechazo': self.motivo_id})

            # 4. Encolamiento eficiente de notificaciones por correo electrónico
            if template:
                local_context = self.env.context.copy()
                for participante in group_users:
                    if participante.email_formatted:
                        if not requiere_filtro_compania or (
                            participante.company_id.identificador_corto == item.company_abreviatura):
                            email_values = {
                                'email_to': participante.email_formatted}
                            template.with_context(local_context).send_mail(
                                item.id, force_send=False,
                                email_values=email_values)

        # redirecciono la salida
        action = self.sudo().env.ref(
            'sicpro_app_transferencias_gastos.transferencias_ordenes_gastos_action').read()[
            0]
        return action