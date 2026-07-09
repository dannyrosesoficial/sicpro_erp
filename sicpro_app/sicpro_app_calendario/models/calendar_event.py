# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from datetime import timedelta

from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import UserError


class Meeting(models.Model):
    _inherit = 'calendar.event'
    _order = "start asc, prioridad desc"

    @api.model
    def _get_default_tipo_sicpro(self):
        """
        Método de búsqueda segura: solo busca si la tabla existe.
        """
        # Verificación de bajo nivel para evitar el error UndefinedTable
        self.env.cr.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'calendar_tipo_calendario'
                )
            """)
        exists = self.env.cr.fetchone()[0]

        if exists:
            tipo = self.env['calendar.tipo.calendario'].search(
                [('tipo_defecto', '=', True)], limit=1)
            return tipo.id if tipo else False
        return False

    start = fields.Datetime(string='Comienza el', required=True, tracking=True,
                            default=fields.Datetime.now,
                            help="Fecha de inicio del evento, sin hora para eventos que duran el día completo")
    stop = fields.Datetime(string='Termina a las', required=True, tracking=True,
                           readonly=False, default=lambda
            self: fields.Datetime.now() + timedelta(hours=1),
                           compute='_compute_stop', store=True,
                           help="Fecha de fin del evento, sin hora para eventos que duran el día completo")
    tipo = fields.Many2one('calendar.tipo.calendario',
                           string="Tipo de actividad",
                           default=_get_default_tipo_sicpro)
    prioridad = fields.Selection(string='Prioridad', related='tipo.prioridad',
                                 store=True)
    participantes_ids = fields.Many2many('sicpro.app.trabajadores.cargos',
                                         'calendarios_cargos_trabajadores_rel',
                                         string='Participantes',
                                         required=False)
    tipo_dvpe = fields.Boolean(string='Inf. DVPE', related='tipo.tipo_dvpe')
    ubicacion = fields.Many2one(comodel_name='sicpro.app.reuniones.lugares',
                                string='Ubicación', required=False)
    actividades_organizativas = fields.Many2one(
        comodel_name='calendar.actividades.organizativas',
        string='Actividades Organizativas', required=False)
    tipo_ubicacion = fields.Selection(string='Tipo Ubicación',
                                      selection=[('otro', 'Otra'),
                                                 ('interno', 'Interna'),
                                                 ('externo', 'Externa'), ],
                                      required=True, default='otro')
    dirige = fields.Many2many('res.users', 'calendar_dirige_res_users_rel',
                              string='Dirige')
    dirige_externos = fields.Many2many('calendar.cargos.externos',
                                       'calendar_dirige_cargos_externos_rel',
                                       string='Dirige Externos')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    cumplimiento_tarea = fields.Selection(string='Cumplimiento',
        selection=[('cumplida', 'Tarea Cumplida'),
                   ('incumplida', 'Tarea Incumplida'), ], required=False, )
    incumplimiento_causa = fields.Text(string="Causa del incumplimiento",
                                       required=False)
    modificacion_tarea = fields.Boolean(string='Tarea modificada',
                                        default=False, )
    modificacion_usuario = fields.Many2many('res.users',
                                            'calendar_modificar_tarea_res_users_rel',
                                            string='Modificaron')
    tipo_tarea = fields.Selection(string='Tipo de Tarea', required=False,
        selection=[('principales', 'Tareas Principales'),
                   ('generales', 'Tareas Generales'), ], )

    # actualizo las actividades organizativas y las paso al nombre del evento
    @api.onchange('actividades_organizativas')
    def onchange_actividades_organizativas(self):
        if self.actividades_organizativas:
            self.name = self.actividades_organizativas.name
            # actualizo a los participantes en dependencia las actividades organizativas
            actividad = self.env['calendar.actividades.organizativas'].search(
                [('name', '=', self.actividades_organizativas.name)])

            # elimino los participantes actuales
            self.partner_ids = None
            # agrego el usuario que crea la actividad
            self.partner_ids = [(4, self.user_id.partner_id.id)]
            # agrego los participantes en dependencia de la actividad
            for usuario in actividad.usuarios_ids:
                self.sudo().partner_ids = [(4, usuario.partner_id.id)]
        else:
            self.name = None
            # elimino los participantes actuales
            self.partner_ids = None
            # agrego el usuario que crea la actividad
            self.partner_ids = [(4, self.user_id.partner_id.id)]

    # actualizo a los participantes en dependencia del cargo seleccionado
    @api.onchange('participantes_ids')
    def plan_dvpe_paticipantes_ids(self):
        cat_ocupacional = self.env['sicpro.app.trabajadores.ocupacion'].search(
            [('name', 'in', self.participantes_ids.ids)])
        trabajadores = self.env['sicpro.app.trabajadores'].search(
            [('ocupacion_id', 'in', cat_ocupacional.ids)]).user_id.partner_id

        # elimino los participantes actuales
        self.partner_ids = None

        # agrego los participantes en dependencia del cargo
        # agrego al organizador
        self.partner_ids = [(4, self.user_id.partner_id.id)]
        # agrego a los trabajadores según el cargo
        for data in trabajadores:
            self.partner_ids = [(4, data.id)]

    ########### Herencias a los métodos de envío de correos ####################
    @api.model_create_multi
    def create(self, vals_list):
        # Prevent sending update notification when _inverse_dates is called
        self = self.with_context(is_calendar_event_new=True)

        vals_list = [
            # Else bug with quick_create when we are filter on an other user
            dict(vals,
                 user_id=self.env.user.id) if not 'user_id' in vals else vals
            for vals in vals_list]

        defaults = self.default_get(
            ['activity_ids', 'res_model_id', 'res_id', 'user_id', 'res_model',
             'partner_ids'])
        meeting_activity_type = self.env['mail.activity.type'].search(
            [('category', '=', 'meeting')], limit=1)
        # get list of models ids and filter out None values directly
        model_ids = list(filter(None, {
            values.get('res_model_id', defaults.get('res_model_id')) for values
            in vals_list}))
        model_name = defaults.get('res_model')
        valid_activity_model_ids = model_name and self.env[
            model_name].sudo().browse(model_ids).filtered(
            lambda m: 'activity_ids' in m).ids or []
        if meeting_activity_type and not defaults.get('activity_ids'):
            for values in vals_list:
                # created from calendar: try to create an activity on the related record
                if values.get('activity_ids'):
                    continue
                res_model_id = values.get('res_model_id',
                                          defaults.get('res_model_id'))
                res_id = values.get('res_id', defaults.get('res_id'))
                user_id = values.get('user_id', defaults.get('user_id'))
                if not res_model_id or not res_id:
                    continue
                if res_model_id not in valid_activity_model_ids:
                    continue
                activity_vals = {'res_model_id': res_model_id,
                                 'res_id': res_id,
                                 'activity_type_id': meeting_activity_type.id, }
                if user_id:
                    activity_vals['user_id'] = user_id
                values['activity_ids'] = [(0, 0, activity_vals)]

        # Add commands to create attendees from partners (if present) if no attendee command
        # is already given (coming from Google event for example).
        # Automatically add the current partner when creating an event if there is none (happens when we quickcreate an event)
        default_partners_ids = defaults.get('partner_ids') or (
        [(4, self.env.user.partner_id.id)])
        vals_list = [dict(vals, attendee_ids=self._attendees_values(
            vals.get('partner_ids', default_partners_ids))) if not vals.get(
            'attendee_ids') else vals for vals in vals_list]
        recurrence_fields = self._get_recurrent_fields()
        recurring_vals = [vals for vals in vals_list if vals.get('recurrency')]
        other_vals = [vals for vals in vals_list if not vals.get('recurrency')]
        events = super().create(other_vals)

        for vals in recurring_vals:
            vals['follow_recurrence'] = True
        recurring_events = super().create(recurring_vals)
        events += recurring_events

        for event, vals in zip(recurring_events, recurring_vals):
            recurrence_values = {field: vals.pop(field) for field in
                                 recurrence_fields if field in vals}
            if vals.get('recurrency'):
                detached_events = event._apply_recurrence_values(
                    recurrence_values)
                detached_events.active = False

        events.filtered(lambda
                            event: event.start > fields.Datetime.now()).attendee_ids._send_mail_to_attendees(
            self.env.ref(
                'sicpro_app_calendario.sicpro_calendar_template_meeting_invitation',
                raise_if_not_found=False))
        events._sync_activities(
            fields={f for vals in vals_list for f in vals.keys()})

        # se deshabilita el envío de correos al crear un evento debido a la recurrencia (demasiados correos 'SPAM')
        # envío el correo electrónico
        # for participantes in events.attendee_ids:
        #     email_values = {'email_to': participantes.partner_id.email_formatted, }
        #     local_context = events.env.context.copy()
        #     template = self.env.ref('sicpro_app_calendario.sicpro_calendar_template_meeting_invitation')
        #     template.with_context(local_context).send_mail(
        #     participantes.id, force_send=True, email_values=email_values)

        if not self.env.context.get('dont_notify'):
            events._setup_alarms()

        return events.with_context(is_calendar_event_new=False)

    def write(self, values):
        detached_events = self.env['calendar.event']
        recurrence_update_setting = values.pop('recurrence_update', None)
        update_recurrence = recurrence_update_setting in (
        'all_events', 'future_events') and len(self) == 1
        break_recurrence = values.get('recurrency') is False

        update_alarms = False
        update_time = False
        if 'partner_ids' in values:
            values['attendee_ids'] = self._attendees_values(
                values['partner_ids'])
            update_alarms = True

        time_fields = self.env['calendar.event']._get_time_fields()
        if any(
            [values.get(key) for key in time_fields]) or 'alarm_ids' in values:
            update_alarms = True
            update_time = True

        if (
            not recurrence_update_setting or recurrence_update_setting == 'self_only' and len(
            self) == 1) and 'follow_recurrence' not in values:
            if any({field: values.get(field) for field in time_fields if
                    field in values}):
                values['follow_recurrence'] = False

        previous_attendees = self.attendee_ids

        recurrence_values = {field: values.pop(field) for field in
                             self._get_recurrent_fields() if field in values}
        if update_recurrence:
            if break_recurrence:
                # Update this event
                detached_events |= self._break_recurrence(
                    future=recurrence_update_setting == 'future_events')
            else:
                future_update_start = self.start if recurrence_update_setting == 'future_events' else None
                time_values = {field: values.pop(field) for field in
                               time_fields if field in values}
                if recurrence_update_setting == 'all_events':
                    # Update all events: we create a new reccurrence and dismiss the existing events
                    self._rewrite_recurrence(values, time_values,
                                             recurrence_values)
                else:
                    # Update future events
                    detached_events |= self._split_recurrence(time_values)
                    self.recurrence_id._write_events(values,
                                                     dtstart=future_update_start)
        else:
            super().write(values)
            self._sync_activities(fields=values.keys())

        # We reapply recurrence for future events and when we add a rrule and 'recurrency' == True on the event
        if recurrence_update_setting not in ['self_only',
                                             'all_events'] and not break_recurrence:
            detached_events |= self._apply_recurrence_values(recurrence_values,
                                                             future=recurrence_update_setting == 'future_events')

        (detached_events & self).active = False
        (detached_events - self).with_context(archive_on_error=True).unlink()

        # Notify attendees if there is an alarm on the modified event, or if there was an alarm
        # that has just been removed, as it might have changed their next event notification
        if not self.env.context.get('dont_notify') and update_alarms:
            self._setup_alarms()
        attendee_update_events = self.filtered(
            lambda ev: ev.user_id != self.env.user)
        if update_time and attendee_update_events:
            # Another user update the event time fields. It should not be auto accepted for the organizer.
            # This prevent weird behavior when a user modified future events time fields and
            # the base event of a recurrence is accepted by the organizer but not the following events
            attendee_update_events.attendee_ids.filtered(
                lambda att: self.user_id.partner_id == att.partner_id).write(
                {'state': 'needsAction'})

        current_attendees = self.filtered('active').attendee_ids
        if 'partner_ids' in values:
            # we send to all partners and not only the new ones
            (current_attendees - previous_attendees)._send_mail_to_attendees(
                self.env.ref(
                    'sicpro_app_calendario.sicpro_calendar_template_meeting_invitation',
                    raise_if_not_found=False))

            # se deshabilita el envío de correos al crear un evento debido a la recurrencia (demasiados correos 'SPAM')  # envío el correo electrónico  # for participantes in self.attendee_ids:  #     email_values = {'email_to': participantes.partner_id.email_formatted, }  #     local_context = self.env.context.copy()  #     template = self.env.ref('sicpro_app_calendario.sicpro_calendar_template_meeting_invitation')  #     template.with_context(local_context).send_mail(  #     participantes.id, force_send=True, email_values=email_values)

        if not self.env.context.get(
            'is_calendar_event_new') and 'start' in values:
            start_date = fields.Datetime.to_datetime(values.get('start'))
            # Only notify on future events
            if start_date and start_date >= fields.Datetime.now():
                (current_attendees & previous_attendees).with_context(
                    calendar_template_ignore_recurrence=not update_recurrence)._send_mail_to_attendees(
                    self.env.ref(
                        'sicpro_app_calendario.sicpro_calendar_template_meeting_changedate',
                        raise_if_not_found=False))
                # envío el correo electrónico
                for participantes in self.attendee_ids:
                    email_values = {
                        'email_to': participantes.partner_id.email_formatted, }
                    local_context = self.env.context.copy()
                    template = self.env.ref(
                        'sicpro_app_calendario.sicpro_calendar_template_meeting_changedate')
                    template.with_context(local_context).send_mail(
                        participantes.id, force_send=True,
                        email_values=email_values)

        return True

    # envía invitación manual a los participantes desde la vista formularios
    def action_sendmail(self):
        email = self.env.user.email
        if email:
            for meeting in self:
                meeting.attendee_ids._send_mail_to_attendees(self.env.ref(
                    'sicpro_app_calendario.sicpro_calendar_template_meeting_invitation',
                    raise_if_not_found=False))

            # envío el correo electrónico
            for participantes in self.attendee_ids:
                email_values = {
                    'email_to': participantes.partner_id.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref(
                    'sicpro_app_calendario.sicpro_calendar_template_meeting_invitation')
                template.with_context(local_context).send_mail(
                    participantes.id, force_send=True,
                    email_values=email_values)
        return True

    # envía invitación manual a los participantes desde la vista de árbol
    def action_open_composer(self):
        if not self.partner_ids:
            raise UserError(
                "No existen participantes en el evento.\n\n" + MSG_SOPORTE_SICPRO)
        template_id = self.env['ir.model.data']._xmlid_to_res_id(
            'sicpro_app_calendario.sicpro_calendar_template_meeting_update',
            raise_if_not_found=False)
        # The mail is sent with datetime corresponding to the sending user TZ
        composition_mode = self.env.context.get('composition_mode', 'comment')
        compose_ctx = dict(default_composition_mode=composition_mode,
                           default_model='calendar.event',
                           default_res_ids=self.ids,
                           default_use_template=bool(template_id),
                           default_template_id=template_id,
                           default_partner_ids=self.partner_ids.ids,
                           mail_tz=self.env.user.tz, )
        return {'type': 'ir.actions.act_window',
                'name': 'Contactar Asistentes', 'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(False, 'form')], 'view_id': False, 'target': 'new',
                'context': compose_ctx, }

        ########### Fin de la Herencias a los métodos de envío de correos ####################

    # envía actualización manual a los participantes desde la vista formularios
    def action_enviar_actualizacion_evento(self):
        if not self.partner_ids:
            raise UserError(
                "No existen participantes en el evento.\n\n" + MSG_SOPORTE_SICPRO)

        email = self.env.user.email
        if email:
            # envío el correo electrónico
            for participantes in self.partner_ids:
                email_values = {'email_to': participantes.email_formatted, }
                local_context = self.env.context.copy()
                template = self.env.ref(
                    'sicpro_app_calendario.sicpro_calendar_template_meeting_update')
                template.with_context(local_context).send_mail(self.id,
                                                               force_send=True,
                                                               email_values=email_values)

        ########### Fin de la Herencias a los métodos de envío de correos ####################
