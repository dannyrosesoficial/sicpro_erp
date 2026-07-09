# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging

import pytz

from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

try:
    import vobject
except ImportError:
    _logger.warning(
        "Módulo Python `vobject` no encontrado, generación de archivos iCal deshabilitada."
        "Considere instalar este módulo si desea generar archivos iCal")
    vobject = None

PRIORIDADES_ACTIVAS = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'),
                       ('3', 'Muy Alta'), ]


class Reuniones(models.Model):
    _name = 'sicpro.app.reuniones'
    _description = 'Gestión de Reuniones'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_inicio desc'

    def _get_default_stage_id(self):
        event_stages = self.env['sicpro.app.reuniones.estados'].search([])
        return event_stages[0] if event_stages else False

    name = fields.Char(string='Nombre de la Reunión', required=True)
    notas = fields.Text(string='Notas')
    active = fields.Boolean(string='Activo', default=True, index=True)
    responsable = fields.Many2one('res.users', string='Responsable',
                                  tracking=True)
    user_id = fields.Many2one('res.users', string='Crea la reunión',
                              tracking=True,
                              default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 change_default=True,
                                 default=lambda self: self.env.company,
                                 required=False)
    fecha_inicio = fields.Datetime(string='Fecha Inicio', required=True,
                                   tracking=True)
    fecha_fin = fields.Datetime(string='Fecha Fin', required=True,
                                tracking=True)
    modelo_reunion = fields.Many2one('sicpro.app.reuniones.etiquetas',
                                     string="Modelo de Reunión", required=True)
    stage_id = fields.Many2one('sicpro.app.reuniones.estados',
                               ondelete='restrict',
                               default=_get_default_stage_id,
                               group_expand='_read_group_stage_ids',
                               tracking=True)
    organizador_id = fields.Many2one('res.users', string='Organizador',
                                     tracking=True,
                                     domain="[('tipo', '=', 'interno')]")
    limitar_participantes = fields.Boolean(string='Limitar participantes',
                                           required=True, readonly=False,
                                           store=True)
    lugar = fields.Many2one(comodel_name='sicpro.app.reuniones.lugares',
                            string='Lugar', required=False,
                            domain=[('tipo', '=', 'interno')])
    lugar_proceso = fields.Many2one('res.company',
                                    string='Dirección del Lugar',
                                    tracking=True, related='lugar.company_id',
                                    store=True)
    lugar_descripcion = fields.Char(string='Descripción',
                                    related='lugar.descripcion', store=True)
    description = fields.Text(string='Descripción detallada de la Reunión',
                              required=True)
    orden_dia = fields.Html(string='Orden del día', required=False,
                            default='<p style="text-align: center;"><b><font style="font-size: 24px;">ORDEN DEL DÍA</font></b></p>')
    prioridad = fields.Selection(PRIORIDADES_ACTIVAS, string='Prioridad',
                                 index=True, tracking=True,
                                 default=PRIORIDADES_ACTIVAS[0][0])
    seats_max = fields.Integer(string='Maximo de participantes',
                               readonly=False, store=True)
    seats_reserved = fields.Integer(string='Asistentes confirmados',
                                    store=True, compute='_compute_seats',
                                    aggregator="sum")
    seats_available = fields.Integer(string='Capacidad disponible', store=True,
                                     readonly=True, compute='_compute_seats')
    seats_unconfirmed = fields.Integer(string='Asistentes no confirmados',
                                       store=True, readonly=True,
                                       compute='_compute_seats')
    seats_used = fields.Integer(string='Participantes', store=True,
                                readonly=True, compute='_compute_seats')
    seats_expected = fields.Integer(string='Asistentes esperados',
                                    compute_sudo=True,
                                    compute='_compute_seats_expected',
                                    aggregator="sum", store=True)
    auto_confirm = fields.Boolean(string='Autoconfirmación', readonly=False,
                                  store=True,
                                  help='Autoconfirm Registrations. Registrations will automatically be confirmed upon creation.')
    participantes_ids = fields.One2many('sicpro.app.reuniones.participantes',
                                        'reunion_id', string='Attendees')

    acuerdos_ids = fields.One2many('sicpro.app.reuniones.acuerdos', 'reunion',
                                   string='Acuerdos', )

    event_registrations_open = fields.Boolean(string='Registration open',
                                              compute='_compute_event_registrations_open',
                                              compute_sudo=True, )
    start_sale_date = fields.Date(string='Start sale date', )
    count_audios = fields.Integer(string='count_audios',
                                  compute='_compute_count_audios_reuniones')
    count_grabaciones = fields.Integer(string='count_grabaciones')
    count_videos = fields.Integer(string='count_videos')
    duracion_reunion = fields.Char(string='Duración reunión',
                                   compute='duracion_reunion_horas',
                                   store=True)
    tipo_reunion = fields.Selection(string='Tipo Reunión',
                                    selection=[('presencial', 'Presencial'),
                                               ('distancia', 'A Distancia'), ],
                                    default='presencial', required=True, )
    modo_distancia = fields.Selection(string='Modo Distancia', selection=[
        ('correo', 'Correo electrónico'), ('audio', 'AudioConferencia'),
        ('video', 'VideoConferencia'), ], required=False, )

    # acción del botón Audio, video, Grabación no hace ninguna función
    def action_empaty_reuniones(self, ):
        action = None

    # calcular la duración de las reuniones
    @api.depends('fecha_fin', 'fecha_inicio')
    def duracion_reunion_horas(self):
        if self.fecha_inicio and self.fecha_fin:
            for duracion in self:
                data = duracion.fecha_fin - duracion.fecha_inicio
                duracion.duracion_reunion = str(
                    round(data.seconds / 60)) + ' Min'

    # contar los archivos de audios guardados
    def _compute_count_audios_reuniones(self):
        attachment_obj = self.env['ir.attachment']
        for audios in self:
            audios.count_audios = attachment_obj.search_count(
                ['&', '&', ('res_model', '=', 'sicpro.app.reuniones'),
                 ('res_id', '=', audios.id), ('mimetype', '=', 'audio/mpeg')])

    # cuenta los participantes por su estado y tipo
    @api.depends('seats_max', 'participantes_ids.state')
    def _compute_seats(self):
        # 1. Inicialización de todos los registros en el recordset para evitar valores nulos
        for event in self:
            event.seats_unconfirmed = 0
            event.seats_reserved = 0
            event.seats_used = 0
            event.seats_available = 0

        state_field = {'draft': 'seats_unconfirmed', 'open': 'seats_reserved',
            'done': 'seats_used'}

        base_vals = dict((fname, 0) for fname in state_field.values())
        results = dict(
            (reunion_id, dict(base_vals)) for reunion_id in self.ids)

        if self.ids:
            # Sincronizamos los datos pendientes en memoria con la base de datos antes de la consulta SQL
            self.env['sicpro.app.reuniones.participantes'].flush_model(
                ['reunion_id', 'state'])

            query = """ SELECT reunion_id, state, count(reunion_id)
                            FROM sicpro_app_reuniones_participantes
                            WHERE reunion_id IN %s AND state IN ('draft', 'open', 'done')
                            GROUP BY reunion_id, state
                        """

            # CORRECCIÓN PARA ODOO 19: Uso de self.env.cr directamente
            self.env.cr.execute(query, (tuple(self.ids),))
            res = self.env.cr.fetchall()

            for reunion_id, state, num in res:
                if reunion_id in results:
                    results[reunion_id][state_field[state]] += num

        # 2. Asignación de los resultados calculados a los campos del objeto
        for event in self:
            res_event = results.get(event.id, base_vals)
            event.seats_unconfirmed = res_event['seats_unconfirmed']
            event.seats_reserved = res_event['seats_reserved']
            event.seats_used = res_event['seats_used']

            # Cálculo de asientos disponibles (lógica de negocio)
            # Se restan los reservados y los confirmados/usados
            if event.seats_max > 0:
                event.seats_available = event.seats_max - (
                        event.seats_reserved + event.seats_used)
            else:
                event.seats_available = 0

    # cuenta los asistentes estimados
    @api.depends('seats_unconfirmed', 'seats_reserved', 'seats_used')
    def _compute_seats_expected(self):
        for event in self:
            event.seats_expected = event.seats_unconfirmed + event.seats_reserved + event.seats_used

    # cuenta los asistentes confirmados
    @api.depends('start_sale_date', 'fecha_fin', 'seats_available',
                 'limitar_participantes')
    def _compute_event_registrations_open(self):
        for event in self:
            current_datetime = fields.Datetime.context_timestamp(event,
                                                                 fields.Datetime.now())
            date_end_tz = event.fecha_fin if event.fecha_fin else False
            event.event_registrations_open = (
                                                 event.start_sale_date <= current_datetime.date() if event.start_sale_date else True) and (
                                                 date_end_tz >= current_datetime if date_end_tz else True) and (
                                                 not event.limitar_participantes or event.seats_available) and (
                                                 not event.acuerdos_ids or any(
                                                 ticket.sale_available for
                                                 ticket in event.acuerdos_ids))

    # chequea la limitación de los participantes
    @api.constrains('seats_max', 'seats_available', 'limitar_participantes')
    def _check_seats_limit(self):
        if any(
            event.limitar_participantes and event.seats_max and event.seats_available < 0
            for event in self):
            raise ValidationError(
                "No existe capacidad para más participantes.\n\n" + MSG_SOPORTE_SICPRO)

    # chequea que la fecha fin no sea anterior a la inicial
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_closing_date(self):
        for event in self:
            if event.fecha_fin < event.fecha_inicio:
                raise ValidationError(
                    "La fecha fin no puede ser anterior a la fecha final.\n\n" + MSG_SOPORTE_SICPRO)

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        return self.env['sicpro.app.reuniones.estados'].sudo().search([])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            computed_values = self._sync_required_computed(vals)
            if computed_values:
                vals.update(computed_values)

        records = super(Reuniones, self).create(vals_list)

        for res in records:
            if res.organizador_id:
                res.message_subscribe([res.organizador_id.id])
        return records

    # enviar notificación del cambio de la reunión a los participantes
    def cambios_reunion(self):
        participantes = self.env['sicpro.app.reuniones.participantes'].search(
            [('reunion_id', '=', self._origin.id)])

        for item in participantes:
            email_values = {'email_to': item.name.email_formatted, }
            # envío el correo a los participantes de la reunión
            local_context = item.env.context.copy()
            template = self.env.ref(
                'sicpro_app_reuniones.reunion_modificicacion_reunion_participante')
            template.with_context(local_context).send_mail(item._origin.id,
                                                           force_send=True,
                                                           email_values=email_values)

    # generar los participantes automáticos de la reunión
    def usuarios_automaticos(self):
        if self.modelo_reunion:
            data = self.env['sicpro.app.reuniones.etiquetas'].search(
                [('id', '=', self.modelo_reunion.id)])
            usuarios = self.modelo_reunion.usuarios_ids

            for items in data.usuarios_ids:
                trabajador = self.env['sicpro.app.trabajadores'].search(
                    [('user_id', '=', items.id)])

                self.env["sicpro.app.reuniones.participantes"].sudo().create(
                    {"name": items.id, "reunion_id": self._origin.id,
                     "phone": trabajador.telefono_trabajo,
                     "mobile": trabajador.movil_trabajo, })

    def write(self, vals):
        res = super(Reuniones, self).write(vals)
        if vals.get('organizador_id'):
            self.message_subscribe([vals['organizador_id']])
        return res

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {}, name="%s (copia)" % (self.name or ''))
        return super(Reuniones, self).copy(default)

    def _sync_required_computed(self, values):
        missing_fields = list(
            set(['limitar_participantes']).difference(set(values.keys())))
        if missing_fields and values:
            cache_event = self.new(values)
            cache_event._compute_seats_limited()
            return dict(
                (fname, cache_event[fname]) for fname in missing_fields)
        else:
            return {}

    def action_set_done(self):
        first_ended_stage = self.env['sicpro.app.reuniones.estados'].search(
            [('pipe_end', '=', True)], order='sequence')
        if first_ended_stage:
            self.write({'stage_id': first_ended_stage[0].id})

    def _get_ics_file(self):
        result = {}
        if not vobject:
            return result

        for event in self:
            cal = vobject.iCalendar()
            cal_event = cal.add('vevent')
            cal_event.add('created').value = fields.Datetime.now().replace(
                tzinfo=pytz.timezone('UTC'))
            cal_event.add('dtstart').value = fields.Datetime.from_string(
                event.fecha_inicio).replace(tzinfo=pytz.timezone('UTC'))
            cal_event.add('dtend').value = fields.Datetime.from_string(
                event.fecha_fin).replace(tzinfo=pytz.timezone('UTC'))
            cal_event.add('summary').value = event.name
            if event.lugar_proceso:
                cal_event.add(
                    'location').value = event.sudo().lugar_proceso.street

            result[event.id] = cal.serialize().encode('utf-8')
        return result

    @api.autovacuum
    def _gc_mark_events_done(self):
        """ move every ended events in the next 'ended stage' """
        ended_events = self.env['sicpro.app.reuniones'].search(
            [('fecha_fin', '<', fields.Datetime.now()),
             ('stage_id.pipe_end', '=', False), ])
        if ended_events:
            ended_events.action_set_done()
