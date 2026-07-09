# -*- coding: utf-8 -*-


from dateutil import rrule

from odoo import api, fields, models, _

MAX_RECURRENT_EVENT = 720

SELECT_FREQ_TO_RRULE = {
    'daily': rrule.DAILY,
    'weekly': rrule.WEEKLY,
    'monthly': rrule.MONTHLY,
    'yearly': rrule.YEARLY,
}

RRULE_FREQ_TO_SELECT = {
    rrule.DAILY: 'daily',
    rrule.WEEKLY: 'weekly',
    rrule.MONTHLY: 'monthly',
    rrule.YEARLY: 'yearly',
}

RRULE_WEEKDAY_TO_FIELD = {
    rrule.MO.weekday: 'mon',
    rrule.TU.weekday: 'tue',
    rrule.WE.weekday: 'wed',
    rrule.TH.weekday: 'thu',
    rrule.FR.weekday: 'fri',
    rrule.SA.weekday: 'sat',
    rrule.SU.weekday: 'sun',
}

RRULE_WEEKDAYS = {'SUN': 'SU', 'MON': 'MO', 'TUE': 'TU', 'WED': 'WE', 'THU': 'TH', 'FRI': 'FR', 'SAT': 'SA'}

RRULE_TYPE_SELECTION = [
    ('daily', 'Días'),
    ('weekly', 'Semanas'),
    ('monthly', 'Meses'),
    ('yearly', 'Años'),
]

END_TYPE_SELECTION = [
    ('count', 'Número de repeticiones'),
    ('end_date', 'Fecha final'),
    ('forever', 'Para siempre'),
]

MONTH_BY_SELECTION = [
    ('date', 'Fecha del mes'),
    ('day', 'Día del mes'),
]

WEEKDAY_SELECTION = [
    ('MON', 'Lunes'),
    ('TUE', 'Martes'),
    ('WED', 'Miércoles'),
    ('THU', 'Jueves'),
    ('FRI', 'Viernes'),
    ('SAT', 'Sábado'),
    ('SUN', 'Domingo'),
]

BYDAY_SELECTION = [
    ('1', 'Primero'),
    ('2', 'Segundo'),
    ('3', 'Tercero'),
    ('4', 'Cuarto'),
    ('-1', 'Ultimo'),
]

def freq_to_select(rrule_freq):
    return RRULE_FREQ_TO_SELECT[rrule_freq]


def freq_to_rrule(freq):
    return SELECT_FREQ_TO_RRULE[freq]


def weekday_to_field(weekday_index):
    return RRULE_WEEKDAY_TO_FIELD.get(weekday_index)


class RecurrenceRule(models.Model):
    _inherit = 'calendar.recurrence'

    rrule_type = fields.Selection(RRULE_TYPE_SELECTION, default='weekly')
    end_type = fields.Selection(END_TYPE_SELECTION, default='count')
    month_by = fields.Selection(MONTH_BY_SELECTION, default='date')
    weekday = fields.Selection(WEEKDAY_SELECTION, string='Weekday')
    byday = fields.Selection(BYDAY_SELECTION, string='By day')


    @api.depends('rrule')
    def _compute_name(self):
        for recurrence in self:
            period = dict(RRULE_TYPE_SELECTION)[recurrence.rrule_type]
            every = _("Cada %(count)s %(period)s", count=recurrence.interval, period=period)

            if recurrence.end_type == 'count':
                end = _("por %s events", recurrence.count)
            elif recurrence.end_type == 'end_date':
                end = _("hasta que %s", recurrence.until)
            else:
                end = ''

            if recurrence.rrule_type == 'weekly':
                weekdays = recurrence._get_week_days()
                # Convert Weekday object
                weekdays = [str(w) for w in weekdays]
                # We need to get the day full name from its three first letters.
                week_map = {v: k for k, v in RRULE_WEEKDAYS.items()}
                weekday_short = [week_map[w] for w in weekdays]
                day_strings = [d[1] for d in WEEKDAY_SELECTION if d[0] in weekday_short]
                on = _("en %s") % ", ".join([day_name for day_name in day_strings])
            elif recurrence.rrule_type == 'monthly':
                if recurrence.month_by == 'day':
                    weekday_label = dict(BYDAY_SELECTION)[recurrence.byday]
                    on = _("sobre el %(position)s %(weekday)s", position=recurrence.byday, weekday=weekday_label)
                else:
                    on = _("día %s", recurrence.day)
            else:
                on = ''
            recurrence.name = ' '.join(filter(lambda s: s, [every, on, end]))
