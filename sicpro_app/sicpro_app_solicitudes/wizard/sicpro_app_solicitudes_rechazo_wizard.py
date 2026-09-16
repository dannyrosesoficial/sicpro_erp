# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models

# NUEVO WIZARD UNIFICADO PARA RECHAZOS Y CANCELACIONES (SIMPLIFICACIÓN)
class SolicitudesMotivoWizard(models.TransientModel):
    _name = 'sicpro.app.solicitudes.motivo.wizard'
    _description = 'Wizard Unificado de Rechazo y Cancelación de Solicitudes'

    action_type = fields.Selection(
        [('cancel_t2', 'Cancelada por Inversionista (T2)'),
         ('cancel_t3', 'Cancelada en la Negociación (T3)'),
         ('reject_t3', 'Rechazada en la Negociación (T3)'),
         ('reject_t4', 'Rechazada por Grupos/Departamento (T4)'),
         ('reject_t5', 'Rechazada por Especialistas (T5)'),
         ('reject_t6', 'Rechazada en la Revisión (T6)'), ],
        string="Tipo de Acción", required=True)

    motivo_cancelacion = fields.Text(string="Motivo de Cancelación")
    lost_reason_id = fields.Many2one('sicpro.app.solicitudes.rechazadas',
                                     string="Motivo de Rechazo")

    def action_procesar(self):
        active_ids = self.env.context.get('active_ids')
        solicitudes = self.env['sicpro.app.solicitudes.oportunidades'].browse(
            active_ids)

        # Mapeo de estados destino
        stage_cancelado = self.env['sicpro.app.solicitudes.estados'].search(
            [('is_cancelado', '=', True)], limit=1).id
        stage_detenido = self.env['sicpro.app.solicitudes.estados'].search(
            [('is_detenido', '=', True)], limit=1).id

        body_msg = 'Iniciativa procesada.'
        action_xml = 'sicpro_app_solicitudes.solicitudes_inversionista_action'

        for sol in solicitudes.sudo():
            if self.action_type == 'cancel_t2':
                sol.motivo_cancelacion = self.motivo_cancelacion
                sol.estado_interno = 'cancelada_cliente'
                sol.stage_id = stage_cancelado
                body_msg = 'Iniciativa cancelada.'
                action_xml = 'sicpro_app_solicitudes.solicitudes_inversionista_action'
                for items in self.env[
                    'sicpro.app.solicitudes.oportunidades'].search(
                    [('solicitud', '=', sol.id)]):
                    items.estado_interno = 'cancelada_cliente'

            elif self.action_type == 'cancel_t3':
                sol.motivo_cancelacion = self.motivo_cancelacion
                sol.estado_interno = 'cancelada_ejecutor'
                sol.stage_id = stage_cancelado
                body_msg = 'Iniciativa cancelada.'
                action_xml = 'sicpro_app_solicitudes.solicitudes_negociacion_action'
                for items in self.env[
                    'sicpro.app.solicitudes.oportunidades'].search(
                    [('solicitud', '=', sol.id)]):
                    items.estado_interno = 'cancelada_ejecutor'

            elif self.action_type == 'reject_t3':
                sol.motivo_rechazo = self.lost_reason_id.id
                sol.estado_interno = 'rechazada_dtp'
                sol.stage_id = stage_detenido
                body_msg = 'Iniciativa rechazada.'
                action_xml = 'sicpro_app_solicitudes.solicitudes_negociacion_action'
                for items in self.env[
                    'sicpro.app.solicitudes.oportunidades'].search(
                    [('solicitud', '=', sol.id)]):
                    items.estado_interno = 'rechazada_dtp'

            elif self.action_type == 'reject_t6':
                sol.motivo_rechazo = self.lost_reason_id.id
                sol.estado_interno = 'rechazada_revision'
                sol.stage_id = stage_detenido
                sol.pg_revisado = True
                sol.pg_rechazado = True
                body_msg = 'Revisión rechazada.'
                action_xml = 'sicpro_app_solicitudes.solicitudes_negociacion_pg_action'
                for items in self.env[
                    'sicpro.app.solicitudes.oportunidades'].search(
                    [('solicitud', '=', sol.id)]):
                    items.estado_interno = 'rechazada_revision'

            elif self.action_type == 'reject_t4':
                sol.motivo_rechazo = self.lost_reason_id.id
                sol.estado_interno = 'rechazada_ejecutor'
                sol.tipo = 'principal'
                sol.rechazada_subsolicitud = True
                sol.stage_id = stage_detenido
                body_msg = 'Iniciativa rechazada.'
                action_xml = 'sicpro_app_solicitudes.solicitudes_ejecutor_action'

            elif self.action_type == 'reject_t5':
                sol.motivo_rechazo = self.lost_reason_id.id
                sol.estado_interno = 'rechazada_agrupacion'
                sol.type = 'iniciativa'
                sol.tipo = 'subsolicitud'
                sol.rechazada_subsolicitud = True
                sol.stage_id = stage_detenido
                body_msg = 'Oportunidad rechazada'
                action_xml = 'sicpro_app_solicitudes.solicitudes_grupos_action'

            # Envío de notificaciones y emails integrados de forma dinámica y genérica
            sol.message_post(body=body_msg, message_type='notification',
                             subtype_xmlid='mail.mt_comment',
                             author_id=self.env.user.partner_id.id)
            for participante in sol.message_partner_ids:
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref(
                    'sicpro_app_solicitudes.solicitudes_cambios_solicitud')
                template.with_context(local_context).send_mail(sol.id,
                                                               force_send=True,
                                                               email_values=email_values)

        return self.env.ref(action_xml).sudo().read()[0]
