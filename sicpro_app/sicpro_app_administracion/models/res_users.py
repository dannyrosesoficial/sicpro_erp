# -*- coding: utf-8 -*-

import logging
from random import randint
from pytz import timezone, UTC
from odoo.tools import format_time
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_partner import SignupError, now

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = 'res.users'

    def _default_color(self):
        return randint(1, 11)

    # resource_id = fields.Many2one('resource.resource')
    # tz = fields.Selection(string='Zona horaria', related='resource_id.tz', readonly=False, )
    estado_usuario = fields.Selection(
        [('present', 'Conectado'), ('absent', 'Ausente'),
         ('to_define', 'Desconocido')], compute='_compute_usuario_state',
        default='to_define', string='Conectividad')
    last_activity = fields.Date(compute="_compute_last_activity")
    last_activity_time = fields.Char(compute="_compute_last_activity")
    user_id = fields.Many2one('res.users')
    color = fields.Integer(string='Color Index',
        default=lambda self: self._default_color())

    @api.depends('im_status')
    def _compute_usuario_state(self):
        # Chequeo el login
        for data in self:
            estado = 'to_define'
            if data.im_status == 'online' or data.last_activity:
                estado = 'present'
            elif data.im_status == 'offline' and data.id:
                estado = 'absent'
            data.estado_usuario = estado

    @api.depends('user_id')
    def _compute_last_activity(self):
        presences = self.env['bus.presence'].search_read(
            [('user_id', 'in', self.mapped('user_id').ids)],
            ['user_id', 'last_presence'])
        # transform the result to a dict with this format {user.id: last_presence}
        presences = {p['user_id'][0]: p['last_presence'] for p in presences}

        for employee in self:
            tz = employee.tz
            last_presence = presences.get(employee.user_id.id, False)
            if last_presence:
                last_activity_datetime = last_presence.replace(
                    tzinfo=UTC).astimezone(timezone(tz)).replace(tzinfo=None)
                employee.last_activity = last_activity_datetime.date()
                if employee.last_activity == fields.Date.context_today(self):
                    employee.last_activity_time = format_time(self.env,
                                                              last_activity_datetime,
                                                              time_format='short')
                else:
                    employee.last_activity_time = False
            else:
                employee.last_activity = False
                employee.last_activity_time = False

    # rescribo función de auth_signup para modificar plantillas
    # de correos  'invitación a sicpro y reset contraseña' a usuarios
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
                template = self.env.ref('sicpro_app_administracion.plantilla_invitacion_sicpro', raise_if_not_found=False)
            except ValueError:
                pass
        if not template:
            template = self.env.ref('sicpro_app_administracion.plantilla_reset_pass_sicpro')
        assert template._name == 'mail.template'

        template_values = {
            'email_to': '${object.email|safe}',
            'email_cc': False,
            'auto_delete': False,
            'partner_to': False,
            'scheduled_date': False,
        }
        template.write(template_values)

        for user in self:
            if not user.email:
                raise UserError(_("Cannot send email: user %s has no email address.", user.name))
            # TDE FIXME: make this template technical (qweb)
            with self.env.cr.savepoint():
                force_send = not(self.env.context.get('import_file', False))
                template.send_mail(user.id, force_send=force_send, raise_exception=True)
            _logger.info("Password reset email sent for user <%s> to <%s>", user.login, user.email)

    # rescribo función de auth_signup para modificar plantilla
    # de correos 'recordatorio de usuarios sin registrar' a usuarios
    def send_unregistered_user_reminder(self, after_days=5):
        datetime_min = fields.Datetime.today() - relativedelta(days=after_days)
        datetime_max = datetime_min + relativedelta(hours=23, minutes=59, seconds=59)

        res_users_with_details = self.env['res.users'].search_read([
            ('share', '=', False),
            ('create_uid.email', '!=', False),
            ('create_date', '>=', datetime_min),
            ('create_date', '<=', datetime_max),
            ('log_ids', '=', False)], ['create_uid', 'name', 'login'])

        # group by invited by
        invited_users = defaultdict(list)
        for user in res_users_with_details:
            invited_users[user.get('create_uid')[0]].append("%s (%s)" % (user.get('name'), user.get('login')))

        # For sending mail to all the invitors about their invited users
        for user in invited_users:
            template = self.env.ref('sicpro_app_administracion.plantilla_recordatorio_invitacion_sicpro').with_context(dbname=self._cr.dbname, invited_users=invited_users[user])
            template.send_mail(user, notif_layout='mail.mail_notification_light', force_send=False)
