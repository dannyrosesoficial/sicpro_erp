# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


# WIZARD UNIFICADO PARA ASIGNACIONES DE GRUPOS Y ESPECIALISTAS
class SolicitudesAsignacionWizard(models.TransientModel):
    _name = 'sicpro.app.solicitudes.asignacion.wizard'
    _description = 'Wizard Unificado de Asignación de Oportunidades'

    assignment_type = fields.Selection(
        [('grupo_t4', 'Asignar a Grupos o Departamento (T4)'),
         ('especialista_t5', 'Transferir entre Especialistas (T5)'), ],
        string="Tipo de Asignación", required=True)

    company_id = fields.Many2one('res.company', string='Proceso',
                                 readonly=True,
                                 default=lambda self: self.env.company.id)
    grupo_ejecutor = fields.Many2one('sicpro.app.trabajadores.areas',
                                     string="Grupo Ejecutor",
                                     domain="[('company_id', '=', company_id)]")
    especialista_ejecutor = fields.Many2one(
        comodel_name="sicpro.app.trabajadores", string='Asignar a',
        required=True)
    ejecucion = fields.Selection([('convertir', 'Convertir a oportunidad'), (
        'fusionar', 'Fusionar con oportunidad existente')],
                                 'Acciones de conversión', default="convertir")

    def action_asignar(self):
        active_ids = self.env.context.get('active_ids')
        oportunidades = self.env[
            'sicpro.app.solicitudes.oportunidades'].browse(active_ids)
        estado_inicial = self.env['sicpro.app.solicitudes.estados'].search(
            [('is_inicial', '=', True)], limit=1).id

        body_msg = 'Proceso Completado.'
        action_xml = 'sicpro_app_solicitudes.solicitudes_ejecutor_action'

        for item in oportunidades.sudo():
            if self.assignment_type == 'grupo_t4':
                item.grupo_ejecutor = self.grupo_ejecutor
                item.especialista_ejecutor = self.especialista_ejecutor
                item.type = 'oportunidad'
                item.fecha_aprobacion = fields.Date.context_today(self)
                if self.especialista_ejecutor:
                    item.stage_id = estado_inicial
                    item.message_subscribe(
                        partner_ids=item.especialista_ejecutor.user_id.partner_id.ids)
                body_msg = 'Oportunidad creada.'
                action_xml = 'sicpro_app_solicitudes.solicitudes_ejecutor_action'

            elif self.assignment_type == 'especialista_t5':
                item.especialista_ejecutante = self.especialista_ejecutor
                if self.especialista_ejecutor:
                    item.stage_id = estado_inicial
                    item.message_subscribe(
                        partner_ids=item.especialista_ejecutante.user_id.partner_id.ids)
                body_msg = 'oportunidad transferida.'
                action_xml = 'sicpro_app_solicitudes.solicitudes_grupos_action'

            item.message_post(body=body_msg, message_type='notification',
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            for participante in item.message_partner_ids:
                email_values = {'email_to': participante.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref(
                    'sicpro_app_solicitudes.solicitudes_cambios_solicitud')
                template.with_context(local_context).send_mail(item.id,
                                                               force_send=True,
                                                               email_values=email_values)

        return self.env.ref(action_xml).sudo().read()[0]
