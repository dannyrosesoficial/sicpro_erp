# -*- coding: utf-8 -*-


from datetime import datetime
import pytz
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class ReunionesParticipantes(models.Model):
    _name = 'sicpro.app.reuniones.participantes'
    _description = 'Participantes de la reunión'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    reunion_id = fields.Many2one('sicpro.app.reuniones', string='Reunión',
                                 required=True, readonly=True,
                                 states={'draft': [('readonly', False)]})

    name = fields.Many2one('res.users', string='Trabajador', tracking=True,
                           domain="[('tipo', '=', 'interno')]")
    email = fields.Char(string='Correo', related='name.email',
                        store=True, tracking=True)
    phone = fields.Char(string='Teléfono',
                        store=True, tracking=True)
    mobile = fields.Char(string='Móvil',
                         store=True, tracking=True)
    company_trabajador = fields.Many2one('res.company', string='Proceso Trabajador',
                                         related='name.company_id', store=True,
                                         tracking=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 related='reunion_id.company_id', store=True,
                                 readonly=True,
                                 states={'draft': [('readonly', False)]})
    fecha_invitacion = fields.Date(
        string='Fecha invitación', readonly=True,
        default=lambda self: fields.Date.context_today(self))
    date_closed = fields.Datetime(string='Fecha finalización',
                                  compute='_compute_date_closed',
                                  readonly=False, store=True)
    fecha_inicio_reunion = fields.Datetime(string="Inicio de reunión",
                                           related='reunion_id.fecha_inicio')
    fecha_fin_reunion = fields.Datetime(string="Fin de reunión",
                                        related='reunion_id.fecha_fin')
    state = fields.Selection(
        [('draft', 'Sin confirmar'), ('cancel', 'Cancelado'),
            ('open', 'Confirmado'), ('done', 'Asistido')], string='Estados',
        default='draft', readonly=True, copy=False, tracking=True)
    tipo_reunion = fields.Selection(string='Tipo Reunión', store=True,
                                    related='reunion_id.tipo_reunion')
    correo_seguidores = fields.Char(string="correo_seguidores", index=True)
    # fechas formateadas
    fecha_invitacion_formated = fields.Char(compute='_fecha_invitacion_formated')
    fecha_inicio_reunion_formated = fields.Char(compute='_fecha_inicio_reunion_formated')
    fecha_fin_reunion_formated = fields.Char(compute='_fecha_fin_reunion_formated')

    def _fecha_invitacion_formated(self):
        for part in self:
            part.fecha_invitacion_formated = part.fecha_invitacion.strftime("%d/%m/%Y")

    def _fecha_inicio_reunion_formated(self):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        for part in self:
            part.fecha_inicio_reunion_formated = datetime.strftime(
                pytz.utc.localize(part.fecha_inicio_reunion).astimezone(local),
                "%d/%m/%Y, %H:%M:%S")

    def _fecha_fin_reunion_formated(self):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        for part in self:
            part.fecha_fin_reunion_formated = datetime.strftime(
                pytz.utc.localize(part.fecha_fin_reunion).astimezone(local),
                "%d/%m/%Y, %H:%M:%S")

    # agregar telefonos del trabajador
    @api.onchange('name')
    def _onchange_name(self):
        self.phone = self.name.trabajador.telefono_trabajo
        self.mobile = self.name.trabajador.movil_trabajo

    # agrego la fecha de terminación de la reunión cuando pase al estado 'done'
    @api.depends('state')
    def _compute_date_closed(self):
        for participante in self:
            if not participante.date_closed:
                if participante.state == 'done':
                    participante.date_closed = fields.Datetime.now()
                else:
                    participante.date_closed = False

    # Verifico la cantidad de capacidades disponibles en la reunión
    @api.constrains('reunion_id', 'state')
    def _check_seats_limit(self):
        for participantes in self:
            if participantes.reunion_id.limitar_participantes and \
                    participantes.reunion_id.seats_max and \
                    participantes.reunion_id.seats_available < (
                    1 if participantes.state == 'draft' else 0):
                raise ValidationError(
                    _('No existe capacidad disponible en la reunión.'))

    # verifico que esta marcada la auto confirmación
    def _check_auto_confirmation(self):
        if any(not registration.reunion_id.auto_confirm or (
                not registration.reunion_id.seats_available and
                registration.reunion_id.limitar_participantes)
               for registration in self):
            return False
        return True

    # cambio al estado borrador
    def action_set_draft(self):
        self.write({'state': 'draft'})

    # cambio al estado abierto
    def action_confirm(self):
        self.write({'state': 'open'})
        # envió la notificación a los seguidores
        self.message_post(body='La Participación ha sido Confirmada',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_app_reuniones.reunion_confirmado_participante')
        template.with_context(local_context).send_mail(self.id, force_send=True)

    # cambio al estado terminado
    def action_set_done(self):
        """ cierra registro """
        self.write({'state': 'done'})

    # cambio al estado cancelado
    def action_cancel(self):
        self.write({'state': 'cancel'})
        # envió la notificación a los seguidores
        self.message_post(body='La participación ha sido Cancelada',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_app_reuniones.reunion_cancelado_participante')
        template.with_context(local_context).send_mail(self.id, force_send=True)


    @api.model_create_multi
    def create(self, vals_list):
        participantes = super(ReunionesParticipantes, self).create(vals_list)
        # si auto confirmo asistencia si esta marcada la opción
        if participantes._check_auto_confirmation():
            participantes.sudo().action_confirm()

        # creo la lista de seguidores
        seguidor = participantes['name']
        # agrego los seguidores al modelo
        participantes.message_subscribe(partner_ids=seguidor.partner_id.ids)
        # envió la notificación a los seguidores
        participantes.message_post(
                body='Ha sido agregado a una nueva reunión',
                message_type='notification', subtype_xmlid='mail.mt_comment',
                author_id=self.env.user.partner_id.id)

        # envío el correo electrónico
        correos = str(seguidor.email_formatted)
        participantes['correo_seguidores'] = correos
        # envío el correo a los seguidores del registro
        template = self.env.ref('sicpro_app_reuniones.reunion_nuevo_participante')
        template.send_mail(participantes.id, force_send=True)

        return participantes