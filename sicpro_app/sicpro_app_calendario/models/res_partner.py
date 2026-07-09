# -*- coding: utf-8 -*-


from odoo import models


class Partner(models.Model):
    _inherit = 'res.partner'

    def get_attendee_detail(self, meeting_ids):

        attendees_details = []
        meetings = self.env['calendar.event'].browse(meeting_ids)
        meetings_attendees = meetings.mapped('attendee_ids')
        for partner in self:
            partner_info = partner.name_get()[0]
            for attendee in meetings_attendees.filtered(lambda att: att.partner_id == partner):
                attendee_is_organizer = self.env.user == attendee.event_id.user_id and attendee.partner_id == self.env.user.partner_id
                attendees_details.append({
                    'id': partner_info[0],
                    'name': partner_info[1],
                    'status': attendee.state,
                    'event_id': attendee.event_id.id,
                    'attendee_id': attendee.id,
                    'is_alone': attendee.event_id.is_organizer_alone and attendee_is_organizer,
                    # attendees data is sorted according to this key in JS.
                    'is_organizer': 1 if attendee.partner_id == attendee.event_id.user_id.partner_id else 0,
                    'prioridad': attendee.event_id.prioridad,
                })
        return attendees_details
