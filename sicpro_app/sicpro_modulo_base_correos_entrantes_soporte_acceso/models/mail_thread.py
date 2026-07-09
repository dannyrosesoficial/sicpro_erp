# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    # método para ejecutar solicitudes de soporte de acceso.
    @api.model
    def metodo_automatiza_correo_soporte_acceso(self, message, message_dict, ruta):
        user_id = ruta['usuario']
        model_id = 'sicpro.app.soporte'
        attachments = message_dict['attachments']
        attachment_ids = []

        body = str(message_dict['body'])
        titulo = body.replace("<pre>", '').replace("</pre>", '')
        descripcion = '<p></p><p><span style="font-weight: bolder; font-size: 18px;">' \
                      'Registro generado automáticamente desde una solicitud de correo electrónico, a continuación sé ' \
                      'adjunta los datos:</span></p><p><span style="font-size: 14px; font-weight: bolder;">' \
                      '<em>Registro del correo:</em></span></p><p>message_type: ' + str(
            message_dict['message_type']) + ',&nbsp;&nbsp; message_id: ' + str(
            message_dict['message_id']) + ',&nbsp;&nbsp; ' \
                                          'subject: ' + str(message_dict['subject']) + ',&nbsp;&nbsp; ' \
                                                                                       'email_from: ' + str(
            message_dict['email_from']) + ',&nbsp;&nbsp; ' \
                                          'from: ' + str(message_dict['from']) + ',&nbsp;&nbsp; ' \
                                                                                 'cc: ' + str(
            message_dict['cc']) + '</p><p>' \
                                  'recipients: ' + str(message_dict['recipients']) + ',&nbsp;' \
                                                                                     '&nbsp; to: ' + str(
            message_dict['to']) + ',&nbsp;&nbsp; ' \
                                  'partner_ids: ' + str(message_dict['partner_ids']) + ',&nbsp;&nbsp; ' \
                                                                                       'references: ' + str(
            message_dict['references']) + ',&nbsp;&nbsp; ' \
                                          'in_reply_to: ' + str(message_dict['in_reply_to']) + ',&nbsp;&nbsp; ' \
                                                                                               'date: ' + str(
            message_dict['date']) + '<br></p><p><font style="color: rgb(99, 0, 0);">' \
                                    '<u>body: ' + str(titulo) + '</u></font><br></p><p>' \
                                                                'bounced_email: ' + str(
            message_dict['bounced_email']) + ',&nbsp;&nbsp; ' \
                                             'bounced_partner: ' + str(
            message_dict['bounced_partner']) + ',&nbsp;&nbsp; ' \
                                               'bounced_msg_id: ' + str(
            message_dict['bounced_msg_id']) + ',&nbsp;&nbsp; ' \
                                              'bounced_message: ' + str(message_dict['bounced_message']) + '<br></p>'

        # diccionario de valores de búsqueda en el cuerpo del mensaje.
        dic = {'NO:', 'No:', 'no:'}
        count = 0
        # Busco la existencia de los valores del diccionario
        for item in dic:
            if item in body:
                indice = body.find(item)
                indice_inicial = indice + 3
                indice_final = indice_inicial + 6
                numero_consecutivo = 'No. ' + str(body[indice_inicial:indice_final])

                # buscar el registro de la solicitud de soporte técnico
                ticket = self.env[model_id].search([('numero_consecutivo', '=', numero_consecutivo)])

                if ticket.id:
                    # Agrego registro del correo a la descripción de ticket
                    ticket.descripcion = ticket.descripcion + descripcion

                    # agrego al creador del correo como seguidor del registro
                    partner_ids = self.env['res.users'].search([('id', '=', user_id)]).partner_id.ids
                    ticket.message_subscribe(partner_ids=list(partner_ids))

                    # cambio el estado del ticket por el que esta pre configurado en la configuración de la app
                    estado_id = self.env['sicpro.app.soporte.estados'].search(
                        [('pendiente_correo_acceso', '=', True)], limit=1).id
                    ticket.stage_id = estado_id

                    # convierto los adjuntos y los agrego al registro
                    values = dict()
                    values.update(
                        {'model': model_id, 'res_id': ticket.id, 'body': titulo, 'partner_ids': partner_ids, })
                    attachments = attachments or []
                    attachment_ids = attachment_ids or []
                    self._message_post_process_attachments(attachments, attachment_ids, values)

                    # actualizo la fecha de recepción de la documentación en las solicitudes
                    id_solicitud = ticket.id_solicitud_acceso
                    solicitud = self.env["sicpro.modulo.plantilla.acceso"].search([('id', '=', id_solicitud)])
                    solicitud.fecha_recibido = datetime.today()

                    # busco al responsable de la distribución
                    responsable = self.env.ref('sicpro_app_soporte.group_soporte_responsable').users
                    # Selecciono el usuario y los administradores
                    notifica = ''
                    for value in responsable:
                        notifica += str(value.email_formatted)

                    # envío el correo electrónico
                    email_values = {'email_to': notifica, }
                    local_context = self.env.context.copy()
                    template = self.env.ref(
                        'sicpro_modulo_base_correos_entrantes_soporte_acceso.soporte_ticket_correcto_solicitud_acceso')
                    template.with_context(local_context).send_mail(ticket.id, force_send=True,
                                                                   email_values=email_values)
                    return ticket
                else:
                    count += 1
            else:
                count += 1

        # verífico la comprobación del diccionario para devolver un mensaje de error.
        if count == 3:
            # busco un, id aleatorio de un ticket para enviar la notificación
            ticket = self.env[model_id].search([], limit=1)

            # busco al responsable de la distribución
            responsable = self.env.ref('sicpro_app_soporte.group_soporte_responsable').users
            # Selecciono el usuario y los administradores
            notifica = ''
            for value in responsable:
                notifica += str(value.email_formatted)
            notifica += str(message_dict['email_from'])

            # envío el correo electrónico
            email_values = {'email_to': notifica, }
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_modulo_base_correos_entrantes_soporte_acceso.soporte_ticket_error_solicitud_acceso')
            template.with_context(local_context).send_mail(ticket.id, force_send=True, email_values=email_values)
