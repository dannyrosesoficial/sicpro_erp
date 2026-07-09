# -*- coding: utf-8 -*-


import datetime
import sys
from datetime import timedelta

import caldav
import icalendar
import pytz
from html2text import html2text
from icalendar import Alarm, vCalAddress, vText

from odoo import api, models, _, fields, Command
from odoo.exceptions import UserError, ValidationError

sys.path.insert(0, "..")
sys.path.insert(0, ".")


class Meeting(models.Model):
    _inherit = 'calendar.event'

    # buscar el url de la aplicación externa
    def caldav_calendario_url(self):
        url = self.env['sicpro.app.administracion.rest.api'].sudo().search(
            [('name', '=', 'sicpro.modulo.calendario.sync')]).url_data
        return url

    # buscar el url de la aplicación externa
    def caldav_conectar(self, usuario, url):
        caldav_url = url + usuario.login + "/"
        try:
            # creo la conexión con el calendario
            cliente = caldav.DAVClient(url=caldav_url, username=usuario.login, password=usuario.nube_token,
                                       ssl_verify_cert=False)

            # provocará la comunicación con el servidor.
            principal = cliente.principal()

        except:
            # Deniego el acceso por la contraseña
            # Desactivo el servicio de calendario del usuario
            usuario.sudo().write({'caldav_calendario_activo': False, 'nube_token_activo': False, 'nube_token': None})
            # Envío notificación para activar el servicio nuevamente
            # busco los usuarios con permisos a recibir los correos alerta
            admin = self.env['res.users'].sudo().search([('groups_id', 'in', self.env.ref(
                'sicpro_app_administracion.grupo_app_administracion_notificaciones').id)])
            # Selecciono los administradores
            notifica = ''
            for value in admin:
                notifica = str(notifica) + str(value.partner_id.email_formatted)
            notifica = str(notifica) + str(usuario.partner_id.email_formatted)
            email_values = {'email_to': notifica, }

            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_modulo_api_calendario.plantilla_calendario_externo_desactivado')
            template.with_context(local_context).send_mail(usuario.id, force_send=True, email_values=email_values)

            calendario = 'Desactivar'
            return calendario

        # verífico que exista el calendario específico
        try:
            # verifico que exista el calendario 'SICPRO ERP' si no lanzo
            # un error para que se cree el calendario automáticamente
            calendario = principal.calendar(name="SICPRO-ERP")
            assert calendario
        except caldav.error.NotFoundError:
            # creo el calendario
            principal.make_calendar(name="SICPRO-ERP")
            return False
        return calendario

    # activo la visualización del la sincronización
    @api.model
    def caldav_sync_manual_calendario_views(self, user_id):
        url = self.caldav_calendario_url()
        if url:
            participantes = self.env['res.users'].browse(user_id)
            if participantes.caldav_calendario_activo:
                return True
            else:
                return False
        else:
            return False

    # sincronizar eventos manuales externos con los del calendario sicpro
    @api.model
    def caldav_sync_manual_calendario(self, user_id):
        # verífico la configuración
        url = self.caldav_calendario_url()
        if url:
            participantes = self.env['res.users'].browse(user_id)

            # compruebo que el usuario tenga la sincronización activa.
            if participantes.caldav_calendario_activo:
                # llamo a la conexión con el calendario del usuario
                calendario = self.caldav_conectar(participantes, url)
                ical = calendario

                # si el calendario no existe en la llamada anterior, lo vuelvo a llamar
                if not ical:
                    calendario = self.caldav_conectar(participantes, url)
                else:
                    # elimino el calendario
                    calendario.delete()
                    calendario = self.caldav_conectar(participantes, url)
                    if not calendario:
                        calendario = self.caldav_conectar(participantes, url)

                # sincronizo los eventos del calendario local en el externo
                asistente = participantes.partner_id.id
                self.caldav_sync_auto_calendario(asistente, calendario)
            else:
                raise ValidationError(_('Usted no está configurado'
                                        ' el calendario remoto.'))
        else:
            raise ValidationError(_('La configuración no está establecida.'))

    # sincronizar eventos externos automáticamente con el calendario sicpro
    def caldav_sync_auto_calendario(self, asistente, calendario):
        # verifico la cantidad de objetos en el calendario
        eventos = self.env['calendar.event'].search([('partner_ids', 'in', asistente)])
        cantidad_eventos_local = len(eventos)
        # compruebo que existan eventos en el calendario SICPRO
        if cantidad_eventos_local > 0:
            for item in eventos:
                try:
                    # Mapeo los campos, creo la conexión y los envío al calendario externo
                    self.mapear_calendario(item, calendario)
                except:
                    raise UserError(_("Ocurrió un error al sincronizar SICPRO ERP con el servidor de calendario "
                                      "externo. Póngase en contacto con el Administrador"))

    # mapear los campos del calendario
    def mapear_calendario(self, item, calendario):
        calendar = icalendar.Calendar()
        event = icalendar.Event()

        # Comienzo a generar el archivo ical
        calendar.add("VERSION", "2.0")
        calendar.add("PRODID", "-//SICPRO ERP//CALENDARIO v1.0//EN")

        timezone = pytz.timezone(self._context.get('tz') or self.env.user.tz or 'UTC')
        now = datetime.datetime.now().astimezone(timezone)

        # identificación del evento
        event.add('uid', str(item.id))
        # prioridad del evento
        event.add('priority', 5)
        # fecha de creación del evento
        event.add("dtstamp", now)

        # verífico si el evento es el día completo
        if item.allday:
            # fecha de inicio del evento
            event.add("dtstart", item.start_date)
            # fecha fin del evento
            event.add("dtend", item.stop_date)
        else:
            # fecha de inicio del evento
            event.add("dtstart", item.start.astimezone(timezone))
            # fecha fin del evento
            event.add("dtend", item.stop.astimezone(timezone))

        # titulo del evento
        event.add("summary", item.name)
        # ubicación del evento
        if item.location:
            event.add('location', item.location)
        # descripción del evento
        if item.description:
            event.add('description', html2text(item.description))
        # url del evento
        if item.videocall_location:
            event.add('url', item.videocall_location)

        # etiquetas del evento
        if item.categ_ids:
            etiquetas = []
            for categorias in item.categ_ids:
                etiquetas.append(categorias.name)
            event.add('categories', etiquetas)

        # libre u ocupado en el evento
        if item.show_as == 'busy':
            # ocupado
            event.add('TRANSP', "OPAQUE")
        elif item.show_as == 'free':
            # libre
            event.add('TRANSP', "TRANSPARENT")

        # recurrencia de ejecución se desactivo debido a que sicpro se ocupa
        # de crear las recurrencias directamente en el calendario externo
        # (Falto por configurar la recurrencia en los meses)
        # if item.recurrency:
        #     ical_rrule = dict()
        #
        #     intervalo = item.recurrence_id.rrule_type
        #     # Repetir cada día
        #     if intervalo == 'daily':
        #         ical_rrule.update(freq='daily')
        #
        #     # Repetir cada semana
        #     if intervalo == 'weekly':
        #         ical_rrule.update(freq='weekly')
        #         dias = []
        #         if item.recurrence_id.mon:
        #             dias.append('MO')
        #         if item.recurrence_id.tue:
        #             dias.append('TU')
        #         if item.recurrence_id.wed:
        #             dias.append('WE')
        #         if item.recurrence_id.thu:
        #             dias.append('TH')
        #         if item.recurrence_id.fri:
        #             dias.append('FR')
        #         if item.recurrence_id.sat:
        #             dias.append('SA')
        #         if item.recurrence_id.sun:
        #             dias.append('SU')
        #         ical_rrule.update(byday=dias)
        #
        #     # Repetir cada mes
        #     if intervalo == 'monthly':
        #         ical_rrule.update(freq='monthly')
        #
        #         dial_mes = item.recurrence_id.month_by
        #         if dial_mes == 'date':
        #             numero_semana = item.recurrence_id.byday
        #             dia_nombre = item.recurrence_id.weekday
        #
        #         if dial_mes == 'day':
        #             dia_numero = item.recurrence_id.day
        #
        #     # Repetir cada año
        #     if intervalo == 'yearly':
        #         ical_rrule.update(freq='yearly')
        #
        #     # intervalo de repetición
        #     ical_rrule.update(interval=item.recurrence_id.interval)
        #
        #     # hasta cuando se realizara las repeticiones
        #     repetir_final = item.recurrence_id.end_type
        #     if repetir_final == 'count':
        #         ical_rrule.update(count=item.recurrence_id.count)
        #     if repetir_final == 'end_date':
        #         ical_rrule.update(until=item.recurrence_id.until)
        #
        #     # envío la configuración de la repetición
        #     event.add("rrule", ical_rrule)

        # organizador del evento

        if item.user_id:
            organizer = vCalAddress('MAILTO:' + item.user_id.email)
            organizer.params['cn'] = vText(item.user_id.name)
            organizer.params['role'] = vText('CHAIR')
            event['organizer'] = organizer

        # participantes de evento
        if item.partner_ids:
            for asistentes in item.partner_ids:
                ical_attendee = vCalAddress('MAILTO:%s' % asistentes.email)
                ical_attendee.params['cn'] = vText(asistentes.name)
                ical_attendee.params['ROLE'] = vText('REQ-PARTICIPANT')
                event.add('attendee', ical_attendee, encode=0)

        # alarma del evento
        if item.alarm_ids:
            for alarm in item.alarm_ids:
                alarma = None
                if alarm.interval == 'minutes':
                    alarma = timedelta(minutes=-int(alarm.duration))
                if alarm.interval == 'hours':
                    alarma = timedelta(hours=-int(alarm.duration))
                if alarm.interval == 'days':
                    alarma = timedelta(days=-int(alarm.duration))
                icalalarm = Alarm()
                icalalarm.add('action', 'DISPLAY')
                icalalarm.add('trigger', alarma)
                event.add_component(icalalarm)

        # guardo los datos del evento
        calendar.add_component(event)
        # guardo el evento en el calendario
        calendario.save_event(calendar)

    # ejecuto este método para la creación o actualización si está activo
    def calendario_local_activado(self, url, calendario, usuario, item, data):
        # si el calendario no existe en la llamada anterior, lo vuelvo a llamar
        sync_calendario = False
        if not calendario:
            sync_calendario = True
            calendario = self.caldav_conectar(usuario, url)

        # En la primera conexión sincronizo los eventos del calendario local en el externo por primera vez
        if sync_calendario:
            asistente = data.id
            self.caldav_sync_auto_calendario(asistente, calendario)
        try:
            # Mapeo los campos, creo la conexión y  los envío al calendario externo
            self.mapear_calendario(item, calendario)
        except:
            raise UserError(_("Ocurrió un error al sincronizar SICPRO ERP con el servidor de calendario externo. "
                              "Póngase en contacto con el Administrador"))

    # ejecuto este método para la eliminación si no está activo
    def calendario_local_desactivado(self, url, usuario, item, calendario):
        caldav_url = url + usuario.login + "/"

        # creo la conexión con el calendario
        cliente = caldav.DAVClient(url=caldav_url, username=usuario.login, password=usuario.nube_token,
                                   ssl_verify_cert=False)
        try:
            # creo el url del evento para eliminar
            url_calendario = cliente.calendar(url=calendario.url)
            ics = str(url_calendario) + str(item.id) + '.ics'

            # Elimino el evento del calendario externo
            caldav.Event(client=cliente, url=str(ics), parent=calendario).delete()
        except:
            raise UserError(_("Ocurrió un error al sincronizar SICPRO ERP con el servidor de calendario externo. "
                              "Póngase en contacto con el Administrador"))

    # crea y actualiza el evento externo al crear registro en el sicpro
    def caldav_crear_actualizar_eliminar_calendario(self, ids, estado):
        # verífico la configuración
        url = self.caldav_calendario_url()
        if url:
            # busco los datos del evento
            evento = self.env['calendar.event'].browse(ids)

            for item in evento:
                for data in item.partner_ids:
                    usuario = self.env['res.users'].search([('partner_id', '=', data.id)])
                    # compruebo que el usuario tenga la sincronización activa.
                    if usuario.caldav_calendario_activo:
                        # llamo a la conexión con el calendario del usuario
                        calendario = self.caldav_conectar(usuario, url)

                        # verífico que el token(pass) de acceso del usuario este actualizado si no deniego la conexión.
                        if calendario != 'Desactivar':
                            # verífico si el estado es para crear/modificar o realizar la eliminación por completo del
                            # calendario local y el calendario externo
                            if estado:
                                # verífico el estado el evento, si está activo ejecuto la creación o actualización.
                                # Si no está activo lo elimino del calendario externo
                                if item.active:
                                    self.calendario_local_activado(url, calendario, usuario, item, data)
                                else:
                                    self.calendario_local_desactivado(url, usuario, item, calendario)
                            else:
                                self.calendario_local_desactivado(url, usuario, item, calendario)
                    else:
                        print('El usuario no está configurado')
        else:
            print('La configuración no está establecida.')

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [dict(vals, user_id=self.env.user.id) if not 'user_id' in vals else vals for vals in vals_list]

        defaults = self.default_get(['activity_ids', 'res_model_id', 'res_id', 'user_id', 'res_model', 'partner_ids'])
        meeting_activity_type = self.env['mail.activity.type'].search([('category', '=', 'meeting')], limit=1)
        # get list of models ids and filter out None values directly
        model_ids = list(
            filter(bool, {values.get('res_model_id', defaults.get('res_model_id')) for values in vals_list}))
        model_name = defaults.get('res_model')
        valid_activity_model_ids = model_name and self.env[model_name].sudo().browse(model_ids).filtered(
            lambda m: 'activity_ids' in m).ids or []
        if meeting_activity_type and not defaults.get('activity_ids'):
            for values in vals_list:
                # created from calendar: try to create an activity on the related record
                if values.get('activity_ids'):
                    continue
                res_model_id = values.get('res_model_id', defaults.get('res_model_id'))
                res_id = values.get('res_id', defaults.get('res_id'))
                user_id = values.get('user_id', defaults.get('user_id'))
                if not res_model_id or not res_id:
                    continue
                if res_model_id not in valid_activity_model_ids:
                    continue
                activity_vals = {'res_model_id': res_model_id, 'res_id': res_id,
                                 'activity_type_id': meeting_activity_type.id, }
                if user_id:
                    activity_vals['user_id'] = user_id
                values['activity_ids'] = [(0, 0, activity_vals)]

        default_partners_ids = defaults.get('partner_ids') or ([(4, self.env.user.partner_id.id)])
        vals_list = [dict(vals, attendee_ids=self._attendees_values(
            vals.get('partner_ids', default_partners_ids))) if not vals.get('attendee_ids') else vals for vals in
                     vals_list]
        recurrence_fields = self._get_recurrent_fields()
        recurring_vals = [vals for vals in vals_list if vals.get('recurrency')]
        other_vals = [vals for vals in vals_list if not vals.get('recurrency')]
        events = super().create(other_vals)

        for vals in recurring_vals:
            vals['follow_recurrence'] = True
        recurring_events = super().create(recurring_vals)
        events += recurring_events

        for event, vals in zip(recurring_events, recurring_vals):
            recurrence_values = {field: vals.pop(field) for field in recurrence_fields if field in vals}
            if vals.get('recurrency'):
                detached_events = event._apply_recurrence_values(recurrence_values)
                detached_events.active = False

        events.filtered(lambda event: event.start > fields.Datetime.now()).attendee_ids._send_mail_to_attendees(
            self.env.ref('calendar.calendar_template_meeting_invitation', raise_if_not_found=False))
        events._sync_activities(fields={f for vals in vals_list for f in vals.keys()})
        if not self.env.context.get('dont_notify'):
            events._setup_alarms()

        # envío él, id y el estado de acción del evento
        # para ejecutar la sincronización
        estado = True
        for item in events:
            evento = item['id']
            events.caldav_crear_actualizar_eliminar_calendario(evento, estado)

        return events

    def write(self, values):
        detached_events = self.env['calendar.event']
        recurrence_update_setting = values.pop('recurrence_update', None)
        update_recurrence = recurrence_update_setting in ('all_events', 'future_events') and len(self) == 1
        break_recurrence = values.get('recurrency') is False

        update_alarms = False
        update_time = False
        if 'partner_ids' in values:
            values['attendee_ids'] = self._attendees_values(values['partner_ids'])
            update_alarms = True

        time_fields = self.env['calendar.event']._get_time_fields()
        if any([values.get(key) for key in time_fields]) or 'alarm_ids' in values:
            update_alarms = True
            update_time = True

        if (not recurrence_update_setting or recurrence_update_setting == 'self_only' and len(
                self) == 1) and 'follow_recurrence' not in values:
            if any({field: values.get(field) for field in time_fields if field in values}):
                values['follow_recurrence'] = False

        previous_attendees = self.attendee_ids

        recurrence_values = {field: values.pop(field) for field in self._get_recurrent_fields() if field in values}
        if update_recurrence:
            if break_recurrence:
                # Update this event
                detached_events |= self._break_recurrence(future=recurrence_update_setting == 'future_events')
            else:
                future_update_start = self.start if recurrence_update_setting == 'future_events' else None
                time_values = {field: values.pop(field) for field in time_fields if field in values}
                if recurrence_update_setting == 'all_events':

                    self._rewrite_recurrence(values, time_values, recurrence_values)
                else:
                    # Update future events
                    detached_events |= self._split_recurrence(time_values)
                    self.recurrence_id._write_events(values, dtstart=future_update_start)
        else:
            super().write(values)
            self._sync_activities(fields=values.keys())

        if recurrence_update_setting not in ['self_only', 'all_events'] and not break_recurrence:
            detached_events |= self._apply_recurrence_values(recurrence_values,
                                                             future=recurrence_update_setting == 'future_events')

        (detached_events & self).active = False
        (detached_events - self).with_context(archive_on_error=True).unlink()
        if not self.env.context.get('dont_notify') and update_alarms:
            self._setup_alarms()
        attendee_update_events = self.filtered(lambda ev: ev.user_id != self.env.user)
        if update_time and attendee_update_events:
            attendee_update_events.attendee_ids.filtered(lambda att: self.user_id.partner_id == att.partner_id).write(
                {'state': 'needsAction'})

        current_attendees = self.filtered('active').attendee_ids
        if 'partner_ids' in values:
            # we send to all partners and not only the new ones
            (current_attendees - previous_attendees)._send_mail_to_attendees(
                self.env.ref('calendar.calendar_template_meeting_invitation', raise_if_not_found=False))
        if 'start' in values:
            start_date = fields.Datetime.to_datetime(values.get('start'))
            # Only notify on future events
            if start_date and start_date >= fields.Datetime.now():
                (current_attendees & previous_attendees).with_context(
                    calendar_template_ignore_recurrence=not update_recurrence)._send_mail_to_attendees(
                    self.env.ref('calendar.calendar_template_meeting_changedate', raise_if_not_found=False))

        # envío él, id y el estado de acción del evento
        # para ejecutar la sincronización
        estado = True
        for item in self:
            evento = item.id
            self.caldav_crear_actualizar_eliminar_calendario(evento, estado)

        return True

    def copy(self, default=None):
        self.ensure_one()
        if not default:
            default = {}

        default.update(partner_ids=[Command.set([])], attendee_ids=[Command.set([])])
        copied_event = super().copy(default)
        copied_event.write({'partner_ids': [(Command.set(self.partner_ids.ids))]})
        return copied_event

    def unlink(self):
        # envío él, id y el estado de acción del evento
        estado = False
        for item in self:
            evento = item.id
            self.caldav_crear_actualizar_eliminar_calendario(evento, estado)

        events = self.filtered_domain([('alarm_ids', '!=', False)])
        partner_ids = events.mapped('partner_ids').ids

        result = super().unlink()
        self.env['calendar.alarm_manager']._notify_next_alarm(partner_ids)

        return result
