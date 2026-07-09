# -*- coding: utf-8 -*-


import logging
import re

from odoo import _, models
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)
_image_dataurl = re.compile(r'(data:image/[a-z]+?);base64,([a-z0-9+/\n]{3,}=*)\n*([\'"])(?: data-filename="([^"]*)")?',
                            re.I)


class Message(models.Model):
    _inherit = 'mail.message'

    def check_access_rule(self, operation):

        def _generate_model_record_ids(msg_val, msg_ids):
            """ :param model_record_ids: {'model': {'res_id': (msg_id, msg_id)}, ... }
                :param message_values: {'msg_id': {'model': .., 'res_id': .., 'author_id': ..}}
            """
            model_record_ids = {}
            for id in msg_ids:
                vals = msg_val.get(id, {})
                if vals.get('model') and vals.get('res_id'):
                    model_record_ids.setdefault(vals['model'], set()).add(vals['res_id'])
            return model_record_ids

        if self.env.is_superuser():
            return
        # Non employees see only messages with a subtype (aka, not internal logs)
        if not self.env['res.users'].has_group('base.group_user'):
            self._cr.execute('''SELECT DISTINCT message.id, message.subtype_id, subtype.internal
                                FROM "%s" AS message
                                LEFT JOIN "mail_message_subtype" as subtype
                                ON message.subtype_id = subtype.id
                                WHERE message.message_type = %%s AND
                                    (message.is_internal IS TRUE OR message.subtype_id IS NULL OR subtype.internal IS TRUE) AND
                                    message.id = ANY (%%s)''' % (self._table),
                             ('comment', self.ids,))
            if self._cr.fetchall():
                raise AccessError(_('No se ha podido completar la operación por restricciones de seguridad. '
                                    'Contacte por favor con su administrador de sistema.\n\n(Tipo de documento: %s, Operación: %s)',
                                    self._description, operation) + ' - ({} {}, {} {})'.format(_('Records:'),
                                                                                               self.ids[:6], _('User:'),
                                                                                               self._uid))

        # Read mail_message.ids to have their values
        message_values = dict((message_id, {}) for message_id in self.ids)

        self.flush(['model', 'res_id', 'author_id', 'parent_id', 'message_type', 'partner_ids'])
        self.env['mail.notification'].flush(['mail_message_id', 'res_partner_id'])

        if operation == 'read':
            self._cr.execute("""
                SELECT DISTINCT m.id, m.model, m.res_id, m.author_id, m.parent_id,
                                COALESCE(partner_rel.res_partner_id, needaction_rel.res_partner_id),
                                m.message_type as message_type
                FROM "%s" m
                LEFT JOIN "mail_message_res_partner_rel" partner_rel
                ON partner_rel.mail_message_id = m.id AND partner_rel.res_partner_id = %%(pid)s
                LEFT JOIN "mail_notification" needaction_rel
                ON needaction_rel.mail_message_id = m.id AND needaction_rel.res_partner_id = %%(pid)s
                WHERE m.id = ANY (%%(ids)s)""" % self._table,
                             dict(pid=self.env.user.partner_id.id,
                                  ids=self.ids))
            for mid, rmod, rid, author_id, parent_id, partner_id, message_type in self._cr.fetchall():
                message_values[mid] = {'model': rmod, 'res_id': rid,
                    'author_id': author_id, 'parent_id': parent_id,
                    'notified': any((message_values[mid].get('notified'), partner_id)), 'message_type': message_type, }
        elif operation == 'write':
            self._cr.execute("""
                SELECT DISTINCT m.id, m.model, m.res_id, m.author_id, m.parent_id,
                                COALESCE(partner_rel.res_partner_id, needaction_rel.res_partner_id),
                                m.message_type as message_type
                FROM "%s" m
                LEFT JOIN "mail_message_res_partner_rel" partner_rel
                ON partner_rel.mail_message_id = m.id AND partner_rel.res_partner_id = %%(pid)s
                LEFT JOIN "mail_notification" needaction_rel
                ON needaction_rel.mail_message_id = m.id AND needaction_rel.res_partner_id = %%(pid)s
                WHERE m.id = ANY (%%(ids)s)""" % self._table,
                             dict(pid=self.env.user.partner_id.id,
                                  uid=self.env.user.id, ids=self.ids))
            for mid, rmod, rid, author_id, parent_id, partner_id, message_type in self._cr.fetchall():
                message_values[mid] = {'model': rmod, 'res_id': rid,
                    'author_id': author_id, 'parent_id': parent_id,
                    'notified': any(
                        (message_values[mid].get('notified'), partner_id)),
                    'message_type': message_type, }
        elif operation in ('create', 'unlink'):
            self._cr.execute(
                """SELECT DISTINCT id, model, res_id, author_id, parent_id, message_type FROM "%s" WHERE id = ANY (%%s)""" % self._table,
                (self.ids,))
            for mid, rmod, rid, author_id, parent_id, message_type in self._cr.fetchall():
                message_values[mid] = {'model': rmod, 'res_id': rid,
                    'author_id': author_id, 'parent_id': parent_id,
                    'message_type': message_type, }
        else:
            raise ValueError(_('Wrong operation name (%s)', operation))

        # Author condition (READ, WRITE, CREATE (private))
        author_ids = []
        if operation == 'read':
            author_ids = [mid for mid, message in message_values.items() if
                          message.get('author_id') and message.get(
                              'author_id') == self.env.user.partner_id.id]
        elif operation == 'write':
            author_ids = [mid for mid, message in message_values.items() if
                          message.get(
                              'author_id') == self.env.user.partner_id.id]
        elif operation == 'create':
            author_ids = [mid for mid, message in message_values.items() if
                          not self.is_thread_message(message)]

        messages_to_check = self.ids
        messages_to_check = set(messages_to_check).difference(set(author_ids))
        if not messages_to_check:
            return

        # Recipients condition, for read and write (partner_ids)
        # keep on top, usefull for systray notifications
        notified_ids = []
        model_record_ids = _generate_model_record_ids(message_values,
                                                      messages_to_check)
        if operation in ['read', 'write']:
            notified_ids = [mid for mid, message in message_values.items() if
                            message.get('notified')]

        messages_to_check = set(messages_to_check).difference(
            set(notified_ids))
        if not messages_to_check:
            return

        # CRUD: Access rights related to the document
        document_related_ids = []
        document_related_candidate_ids = [mid for mid, message in
            message_values.items() if (message.get('model') and message.get(
                'res_id') and message.get(
                'message_type') != 'user_notification')]
        model_record_ids = _generate_model_record_ids(message_values,
                                                      document_related_candidate_ids)
        for model, doc_ids in model_record_ids.items():
            DocumentModel = self.env[model]
            if hasattr(DocumentModel, '_get_mail_message_access'):
                check_operation = DocumentModel._get_mail_message_access(
                    doc_ids, operation)  ## why not giving model here?
            else:
                check_operation = self.env[
                    'mail.thread']._get_mail_message_access(doc_ids, operation,
                                                            model_name=model)
            records = DocumentModel.browse(doc_ids)
            records.check_access_rights(check_operation)
            mids = records.browse(doc_ids)._filter_access_rules(
                check_operation)
            document_related_ids += [mid for mid, message in
                message_values.items() if (
                        message.get('model') == model and message.get(
                    'res_id') in mids.ids and message.get(
                    'message_type') != 'user_notification')]

        messages_to_check = messages_to_check.difference(
            set(document_related_ids))

        if not messages_to_check:
            return

        # Parent condition, for create (check for received notifications for the created message parent)
        notified_ids = []
        if operation == 'create':
            # TDE: probably clean me
            parent_ids = [message.get('parent_id') for message in
                          message_values.values() if message.get('parent_id')]
            self._cr.execute("""SELECT DISTINCT m.id, partner_rel.res_partner_id FROM "%s" m
                LEFT JOIN "mail_message_res_partner_rel" partner_rel
                ON partner_rel.mail_message_id = m.id AND partner_rel.res_partner_id = (%%s)
                WHERE m.id = ANY (%%s)""" % self._table,
                             (self.env.user.partner_id.id, parent_ids,))
            not_parent_ids = [mid[0] for mid in self._cr.fetchall() if mid[1]]
            notified_ids += [mid for mid, message in message_values.items() if
                             message.get('parent_id') in not_parent_ids]

        messages_to_check = messages_to_check.difference(set(notified_ids))
        if not messages_to_check:
            return

        # Recipients condition for create (message_follower_ids)
        if operation == 'create':
            for doc_model, doc_ids in model_record_ids.items():
                followers = self.env['mail.followers'].sudo().search(
                    [('res_model', '=', doc_model),
                        ('res_id', 'in', list(doc_ids)),
                        ('partner_id', '=', self.env.user.partner_id.id), ])
                fol_mids = [follower.res_id for follower in followers]
                notified_ids += [mid for mid, message in message_values.items()
                                 if message.get(
                        'model') == doc_model and message.get(
                        'res_id') in fol_mids and message.get(
                        'message_type') != 'user_notification']

        messages_to_check = messages_to_check.difference(set(notified_ids))
        if not messages_to_check:
            return

        if not self.browse(messages_to_check).exists():
            return

        # Doy acceso a visualizar los correos que son del usuario (Public) al grupo: administrador sicpro erp
        if not self.env['res.users'].has_group(
                'sicpro_app_administracion.grupo_app_administracion_admin'):
            raise AccessError(
                _('No se ha podido completar la operación por restricciones de seguridad. '
                  'Contacte por favor con su administrador de sistema.\n\n(Tipo de documento: %s, Operación: %s)',
                  self._description, operation) + ' - ({} {}, {} {})'.format(
                    _('Records:'), list(messages_to_check)[:6], _('User:'),
                    self._uid))
