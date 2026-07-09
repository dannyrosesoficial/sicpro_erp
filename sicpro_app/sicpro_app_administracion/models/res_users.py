# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
from random import randint

from dateutil.relativedelta import relativedelta
from pytz import timezone, UTC

from odoo import api, fields, models, _
from odoo.addons.auth_signup.models.res_partner import now
from odoo.exceptions import UserError
from odoo.tools import format_time

_logger = logging.getLogger(__name__)


def _default_color():
    return randint(1, 11)


class Users(models.Model):
    _inherit = 'res.users'

    status = fields.Selection(selection=[('done', 'En Linea'), ('blocked', 'Desconectado'), ], default='blocked',
                              string="Estado del Usuario", compute='_compute_usuario_state', store=True)
    identificador_corto = fields.Char(string='Proceso Corto', required=False, related='company_id.identificador_corto')

    last_activity = fields.Date(compute="_compute_last_activity")
    last_activity_time = fields.Char(compute="_compute_last_activity")
    user_id = fields.Many2one('res.users')
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    @api.depends('im_status')
    def _compute_usuario_state(self):
        # Chequeo el login
        for item in self:
            estado = 'blocked'
            if item.im_status == 'online':
                estado = 'done'
            elif item.im_status == 'offline':
                estado = 'blocked'
            item.status = estado

    @api.depends('user_id')
    def _compute_last_activity(self):
        presencia = self.env['bus.presence'].search_read([('user_id', 'in', self.ids)], ['user_id', 'last_presence'])

        presencia = {p['user_id'][0]: p['last_presence'] for p in presencia}

        for usuario in self:
            tz = usuario.tz
            last_presence = presencia.get(usuario.id, False)

            if last_presence:
                last_activity_datetime = last_presence.replace(tzinfo=UTC).astimezone(timezone(tz)).replace(tzinfo=None)
                usuario.last_activity = last_activity_datetime.date()

                if usuario.last_activity == fields.Date.context_today(self):
                    usuario.last_activity_time = format_time(self.env, last_activity_datetime, time_format='short')
                else:
                    usuario.last_activity_time = False
            else:
                usuario.last_activity = False
                usuario.last_activity_time = False

    # rescribo función de auth_signup para modificar plantillas de correos 'invitación a sicpro
    # y reset contraseña' a usuarios
    def action_reset_password(self):
        """ create signup token for each user, and send their signup
        url by email """
        if self.env.context.get('install_mode', False):
            return
        if self.filtered(lambda user: not user.active):
            raise UserError(_("You cannot perform this action on an archived user."))
        # prepare reset password signup
        create_mode = bool(self.env.context.get('create_user'))

        # no time limit for initial invitation, only for reset password
        expiration = False if create_mode else now(days=+1)

        self.mapped('partner_id').signup_prepare(signup_type="reset", expiration=expiration)

        # send email to users with their signup url
        template = False
        if create_mode:
            try:
                template = self.env.ref('sicpro_app_administracion.plantilla_invitacion_sicpro',
                                        raise_if_not_found=False)
            except ValueError:
                pass
        if not template:
            template = self.env.ref('sicpro_app_administracion.plantilla_reset_pass_sicpro')
        assert template._name == 'mail.template'

        template_values = {'email_to': '{{ object.email }}', 'email_cc': False, 'auto_delete': False,
            'partner_to': False, 'scheduled_date': False, }
        template.write(template_values)

        for user in self:
            if not user.email:
                raise UserError(_("Cannot send email: user %s has no email address.", user.name))
            # TDE FIXME: make this template technical (qweb)
            with self.env.cr.savepoint():
                force_send = not (self.env.context.get('import_file', False))
                template.send_mail(user.id, force_send=force_send, raise_exception=True)
            _logger.info("Password reset email sent for user <%s> to <%s>", user.login, user.email)

    # rescribo función de auth_signup para modificar plantilla de correos 'recordatorio de
    # usuarios sin registrar' a usuarios
    def send_unregistered_user_reminder(self, after_days=5):
        datetime_min = fields.Datetime.today() - relativedelta(days=after_days)
        datetime_max = datetime_min + relativedelta(hours=23, minutes=59, seconds=59)

        res_users_with_details = self.env['res.users'].search_read(
            [('share', '=', False), ('create_uid.email', '!=', False), ('create_date', '>=', datetime_min),
                ('create_date', '<=', datetime_max), ('log_ids', '=', False)], ['create_uid', 'name', 'login'])

        # group by invited by
        invited_users = defaultdict(list)
        for user in res_users_with_details:
            invited_users[user.get('create_uid')[0]].append("%s (%s)" % (user.get('name'), user.get('login')))

        # For sending mail to all the invitors about their invited users
        for user in invited_users:
            template = self.env.ref('sicpro_app_administracion.plantilla_recordatorio_invitacion_sicpro').with_context(
                dbname=self._cr.dbname, invited_users=invited_users[user])
            template.send_mail(user, notif_layout='mail.mail_notification_light', force_send=False)

    # envío el correo de invitación a los usuarios
    def enviar_invitacion_usuario(self):
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_app_administracion.plantilla_invitacion_sicpro')
        template.with_context(local_context).send_mail(self.id, force_send=True)

    # envío el correo de actualización de los roles a los usuarios
    def enviar_actualizacion_roles(self):
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_app_administracion.plantilla_actualizacion_roles')
        template.with_context(local_context).send_mail(self.id, force_send=True)
