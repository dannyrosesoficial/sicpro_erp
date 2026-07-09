# -*- coding: utf-8 -*-


from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    # método para ejecutar solicitudes de soporte técnico.
    @api.model
    def metodo_automatiza_correo_soporte_tecnico(self, message, message_dict, ruta):
        user_id = ruta['usuario']
        model_id = 'sicpro.app.soporte'
        attachments = message_dict['attachments']
        attachment_ids = []

        body = str(message_dict['body'])
        titulo = body.replace("<pre>", '').replace("</pre>", '')
        descripcion = '<p><span style="font-weight: bolder; font-size: 18px;">' \
                      'Ticket generado automáticamente desde una solicitud de correo electrónico, a continuación sé ' \
                      'adjunta el registro:</span></p><p><span style="font-size: 14px; font-weight: bolder;">' \
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

        # buscar el canal de comunicación
        canal = self.env['sicpro.app.soporte.canales'].search([('code', '=', 'correo_electronico')]).id

        # creo el registro de la solicitud de soporte técnico
        ticket = self.env[model_id].create(
            {'name': titulo, 'partner_user_id': user_id, 'channel_id': canal, 'descripcion': descripcion, })

        # agrego al creador del correo como seguidor del registro
        partner_ids = self.env['res.users'].search([('id', '=', user_id)]).partner_id.ids
        ticket.message_subscribe(partner_ids=list(partner_ids))

        # convierto los adjuntos y los agrego al registro
        values = dict()
        values.update({'model': model_id, 'res_id': ticket.id, 'body': titulo, 'partner_ids': partner_ids, })
        attachments = attachments or []
        attachment_ids = attachment_ids or []
        self._message_post_process_attachments(attachments, attachment_ids, values)

        return ticket
