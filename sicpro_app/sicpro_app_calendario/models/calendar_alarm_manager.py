# -*- coding: utf-8 -*-


import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class AlarmManager(models.AbstractModel):
    _inherit = 'calendar.alarm_manager'

    @api.model
    def _send_reminder(self):
        # Ejecutar via cron
        events_by_alarm = self._get_events_by_alarm_to_notify('email')
        if not events_by_alarm:
            return

        event_ids = list(set(event_id for event_ids in events_by_alarm.values() for event_id in event_ids))
        events = self.env['calendar.event'].browse(event_ids)
        attendees = events.attendee_ids.filtered(lambda a: a.state != 'declined')

        alarms = self.env['calendar.alarm'].browse(events_by_alarm.keys())
        template = self.env.ref('sicpro_app_calendario.sicpro_calendar_template_meeting_reminder')

        for alarm in alarms:
            alarm_attendees = attendees.filtered(lambda attendee: attendee.event_id.id in events_by_alarm[alarm.id])
            # alarm_attendees.with_context(
            #     mail_notify_force_send=True, calendar_template_ignore_recurrence=True
            # )._send_mail_to_attendees(alarm.mail_template_id, force_send=True)
            alarm_attendees.with_context(mail_notify_force_send = True, calendar_template_ignore_recurrence = True
                                         )._send_mail_to_attendees(template, force_send=True)

            # envío el correo electrónico
            for participantes in alarm_attendees:
                email_values = {'email_to': participantes.partner_id.email_formatted, }
                local_context = self.env.context.copy()
                template.with_context(local_context).send_mail(participantes.id, force_send=True,
                                                               email_values=email_values)
