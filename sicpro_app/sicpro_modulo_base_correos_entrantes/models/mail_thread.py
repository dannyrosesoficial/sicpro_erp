# -*- coding: utf-8 -*-


import email
import email.policy
import logging
from xmlrpc import client as xmlrpclib

from odoo import api, models

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    # Recibe el mensaje de correo electrónico para ser procesado
    def message_process_aplicaciones(self, model, message, custom_values=None, save_original=False,
                                     strip_attachments=False, thread_id=None):
        # extraer bytes del mensaje: nos vemos obligados a pasar el mensaje como binario
        # porque no conocemos su codificación hasta que analizamos sus encabezados y, por lo tanto,
        # no podemos convertirlo a utf-8 para el transporte entre el script de mailgate y aquí.
        if isinstance(message, xmlrpclib.Binary):
            message = bytes(message.data)
        if isinstance(message, str):
            message = message.encode('utf-8')
        message = email.message_from_bytes(message, policy=email.policy.SMTP)

        # analice el mensaje, verifique que no estamos en un bucle al verificar que message_id no esté duplicado
        msg_dict = self.message_parse(message, save_original=save_original)
        if strip_attachments:
            msg_dict.pop('attachments', None)

        existing_msg_ids = self.env['mail.message'].search([('message_id', '=', msg_dict['message_id'])], limit=1)
        if existing_msg_ids:
            _logger.info('Correo ignorado de %s a %s con ID de mensaje %s: '
                         'se encontró un, Id. de mensaje duplicado durante el procesamiento',
                         msg_dict.get('email_from'), msg_dict.get('to'), msg_dict.get('message_id'))
            return False

        # encontrar posibles rutas para el mensaje
        ruta = self.message_route_aplicaciones(msg_dict)
        thread_id = self._message_route_process_aplicaciones(message, msg_dict, ruta)
        return thread_id

    # Devuelve el nombre del método que será ejecutado y el usuario que envía el correo
    @api.model
    def message_route_aplicaciones(self, message_dict):
        email_correo = message_dict['email_from']
        email_asunto = message_dict['subject']
        usuario = self._mail_find_user_for_gateway(email_correo).id or self._mail_find_user_for_gateway('sicproerp@etecsa.cu').id
        metodos_ids = self.env['sicpro.modulo.base.correos.entrantes.metodos'].search([('asunto', '=', email_asunto)])
        metodo = None
        ruta = []

        # busco si el asunto existe el registro de control para encontrar el método a ejecutar
        for item in metodos_ids:
            asunto_ids = item.asunto
            for value in asunto_ids:
                if value.name == str(email_asunto):
                    metodo = item.name

        ruta = {'metodo': metodo, 'usuario': usuario}
        return ruta

    # Ejecuta el método que solicitado
    @api.model
    def _message_route_process_aplicaciones(self, message, message_dict, ruta):
        metodo = str(ruta['metodo'])

        # Compruebo si existe el método y lo ejecuto
        if metodo != 'None':
            metodo_str = 'self.' + metodo + '(message, message_dict, ruta)'
            run_method = eval(metodo_str)
            _logger.info('El Método ' + metodo_str + ' ha sido ejecutado')
            return run_method
        else:
            # de momento si no está registrado el asunto no se ejecutara ninguna función
            _logger.info('El asunto del correo no tiene identificador creado')

    @api.model
    def metodo_automatiza_soporte_original(self, message, message_dict, routes):
        self = self.with_context(attachments_mime_plainxml=True)  # importar archivos adjuntos XML como texto
        # posponga la configuración de message_dict.partner_ids después de message_post,
        # para evitar notificaciones dobles
        original_partner_ids = message_dict.pop('partner_ids', [])
        thread_id = False
        for model, thread_id, custom_values, user_id, alias in routes or ():
            subtype_id = False
            related_user = self.env['res.users'].browse(user_id)
            Model = self.env[model].with_context(mail_create_nosubscribe=True, mail_create_nolog=True)
            if not (thread_id and hasattr(Model, 'message_update') or hasattr(Model, 'message_new')):
                raise ValueError("Undeliverable mail with Message-Id %s, model %s does not accept incoming emails" % (
                message_dict['message_id'], model))

            # disabled subscriptions during message_new/update to avoid having the system user running the
            # email gateway become a follower of all inbound messages
            ModelCtx = Model.with_user(related_user).sudo()
            if thread_id and hasattr(ModelCtx, 'message_update'):
                thread = ModelCtx.browse(thread_id)
                thread.message_update(message_dict)
            else:
                # if a new thread is created, parent is irrelevant
                message_dict.pop('parent_id', None)
                thread = ModelCtx.message_new(message_dict, custom_values)
                thread_id = thread.id
                subtype_id = thread._creation_subtype().id

            # replies to internal message are considered as notes, but parent message
            # author is added in recipients to ensure he is notified of a private answer
            parent_message = False
            if message_dict.get('parent_id'):
                parent_message = self.env['mail.message'].sudo().browse(message_dict['parent_id'])
            partner_ids = []
            if not subtype_id:
                if message_dict.get('is_internal'):
                    subtype_id = self.env['ir.model.data']._xmlid_to_res_id('mail.mt_note')
                    if parent_message and parent_message.author_id:
                        partner_ids = [parent_message.author_id.id]
                else:
                    subtype_id = self.env['ir.model.data']._xmlid_to_res_id('mail.mt_comment')

            post_params = dict(subtype_id=subtype_id, partner_ids=partner_ids, **message_dict)
            # remove computational values not stored on mail.message and avoid warnings when creating it
            for x in ('from', 'to', 'cc', 'recipients', 'references', 'in_reply_to', 'bounced_email', 'bounced_message',
                      'bounced_msg_id', 'bounced_partner'):
                post_params.pop(x, None)
            new_msg = False
            if thread._name == 'mail.thread':  # message with parent_id not linked to record
                new_msg = thread.message_notify(**post_params)
            else:
                # parsing should find an author independently of user running mail gateway, and ensure it is not odoobot
                partner_from_found = message_dict.get('author_id') and message_dict['author_id'] != self.env[
                    'ir.model.data']._xmlid_to_res_id('base.partner_root')
                thread = thread.with_context(mail_create_nosubscribe=not partner_from_found)
                new_msg = thread.message_post(**post_params)

            if new_msg and original_partner_ids:
                # postponed after message_post, because this is an external message and we don't want to create
                # duplicate emails due to notifications
                new_msg.write({'partner_ids': original_partner_ids})
        return thread_id