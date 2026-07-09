# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging
from random import randint

from dateutil.relativedelta import relativedelta
from pytz import timezone, UTC
from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import UserError
from odoo.tools import format_time

_logger = logging.getLogger(__name__)


def _default_color():
    return randint(1, 11)


class Users(models.Model):
    _inherit = 'res.users'

    status = fields.Selection(
        selection=[('done', 'En Linea'), ('blocked', 'Desconectado'), ],
        default='blocked', string="Estado del Usuario",
        compute='_compute_usuario_state', store=True)
    identificador_corto = fields.Char(string='Proceso Corto', required=False,
                                      related='company_id.identificador_corto')

    last_activity = fields.Date(compute="_compute_last_activity")
    last_activity_time = fields.Char(compute="_compute_last_activity")
    user_id = fields.Many2one('res.users')
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

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
        for usuario in self:
            tz = usuario.tz
            # sudo: res.users - can access presence of accessible user
            if last_presence := usuario.user_id.sudo().presence_ids.last_presence:
                last_activity_datetime = last_presence.replace(
                    tzinfo=UTC).astimezone(timezone(tz)).replace(tzinfo=None)
                usuario.last_activity = last_activity_datetime.date()
                if usuario.last_activity == fields.Date.today():
                    usuario.last_activity_time = format_time(self.env,
                                                             last_presence,
                                                             time_format='short')
                else:
                    usuario.last_activity_time = False
            else:
                usuario.last_activity = False
                usuario.last_activity_time = False

    # rescribo función de auth_signup para modificar plantillas de correos 'invitación a sicpro
    # y reset contraseña' a usuarios
    def action_reset_password(self, signup_type="reset"):
        if self.env.context.get('install_mode', False):
            return
        if self.filtered(lambda user: not user.active):
            raise UserError(
                "No puedes realizar esta acción en un usuario archivado.\n\n" + MSG_SOPORTE_SICPRO)
        # prepare reset password signup
        create_mode = bool(self.env.context.get('create_user'))

        self.mapped('partner_id').signup_prepare(signup_type=signup_type)

        # send email to users with their signup url
        template = False
        if create_mode:
            try:
                template = self.env.ref(
                    'sicpro_app_administracion.plantilla_invitacion_sicpro',
                    raise_if_not_found=False)
            except ValueError:
                pass
        if not template:
            template = self.env.ref(
                'sicpro_app_administracion.plantilla_reset_pass_sicpro')
        assert template._name == 'mail.template'

        template_values = {'email_to': '{{ object.email }}', 'email_cc': False,
                           'auto_delete': False, 'partner_to': False,
                           'scheduled_date': False, }
        template.write(template_values)

        for user in self:
            if not user.email:
                raise UserError(
                    "No se puede enviar correo electrónico: el usuario %s no tiene dirección de correo electrónico.\n\n" % user.name + MSG_SOPORTE_SICPRO)
            # TDE FIXME: make this template technical (qweb)
            with self.env.cr.savepoint():
                force_send = not (self.env.context.get('import_file', False))
                template.send_mail(user.id, force_send=force_send,
                                   raise_exception=True)
            _logger.info("Password reset email sent for user <%s> to <%s>",
                         user.login, user.email)

    # rescribo función de auth_signup para modificar plantilla de correos 'recordatorio de
    # usuarios sin registrar' a usuarios
    def send_unregistered_user_reminder(self, *, after_days=5, batch_size=100):
        email_template = self.env.ref('sicpro_app_administracion.plantilla_recordatorio_invitacion_sicpro', raise_if_not_found=False)
        if not email_template:
            _logger.warning("No se encontró la plantilla 'plantilla_recordatorio_invitacion_sicpro'. No se pueden enviar notificaciones de recordatorio.")
            self.env['ir.cron']._commit_progress(deactivate=True)
            return
        datetime_min = fields.Datetime.today() - relativedelta(days=after_days)
        datetime_max = datetime_min + relativedelta(days=1)

        invited_by_users = self.search_fetch([
            ('share', '=', False),
            ('create_uid.email', '!=', False),
            ('create_date', '>=', datetime_min),
            ('create_date', '<', datetime_max),
            ('log_ids', '=', False),
        ], ['name', 'login', 'create_uid']).grouped('create_uid')

        for user, invited_users in invited_by_users.items():
            invited_user_emails = [f"{u.name} ({u.login})" for u in invited_users]
            template = email_template.with_context(dbname=self.env.cr.dbname, invited_users=invited_user_emails)
            template.send_mail(user.id, email_layout_xmlid='mail.mail_notification_light', force_send=False)
            if not self.env['ir.cron']._commit_progress(len(invited_users)):
                _logger.info("Envío de invitación a usuarios: tiempo de "
                             "espera alcanzado, "
                             "deteniéndose")
                break

    # envío el correo de invitación a los usuarios
    def enviar_invitacion_usuario(self):
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_app_administracion.plantilla_invitacion_sicpro')
        template.with_context(local_context).send_mail(self.id,
                                                       force_send=True)

    # envío el correo de actualización de los roles a los usuarios
    def enviar_actualizacion_roles(self):
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_app_administracion.plantilla_actualizacion_roles')
        template.with_context(local_context).send_mail(self.id,
                                                       force_send=True)
