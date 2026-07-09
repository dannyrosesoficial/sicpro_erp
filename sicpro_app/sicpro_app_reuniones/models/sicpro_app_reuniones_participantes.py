# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class ReunionesParticipantes(models.Model):
    _name = 'sicpro.app.reuniones.participantes'
    _description = 'Participantes de la reunión'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    reunion_id = fields.Many2one('sicpro.app.reuniones', string='Reunión',
                                 required=True, readonly=True)
    name = fields.Many2one('res.users', string='Trabajador', tracking=True,
                           domain="[('tipo', '=', 'interno')]")
    email = fields.Char(string='Correo', related='name.email', store=True,
                        tracking=True)
    phone = fields.Char(string='Teléfono', store=True, tracking=True)
    mobile = fields.Char(string='Móvil', store=True, tracking=True)
    company_trabajador = fields.Many2one('res.company',
                                         string='Proceso Trabajador',
                                         related='name.company_id', store=True,
                                         tracking=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 related='reunion_id.company_id', store=True,
                                 readonly=True, )
    fecha_invitacion = fields.Date(string='Fecha invitación', readonly=True,
                                   default=lambda
                                       self: fields.Date.context_today(self))
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

    # agregar teléfonos del trabajador
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

    # Verífico la cantidad de capacidades disponibles en la reunión
    @api.constrains('reunion_id', 'state')
    def _check_seats_limit(self):
        for participantes in self:
            if participantes.reunion_id.limitar_participantes and participantes.reunion_id.seats_max and participantes.reunion_id.seats_available < (
                1 if participantes.state == 'draft' else 0):
                raise ValidationError(
                    'No existe capacidad disponible en la reunión.' + MSG_SOPORTE_SICPRO)

    # verifico que esta marcada la auto confirmación
    def _check_auto_confirmation(self):
        if any(not registration.reunion_id.auto_confirm or (
            not registration.reunion_id.seats_available and registration.reunion_id.limitar_participantes)
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
        self.message_post(body='Participación Confirmada',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # envío los correo de los seguidores del registro
        for participantes in self.message_partner_ids:
            # envío el correo a los seguidores del registro
            email_values = {'email_to': participantes.email_formatted}
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_reuniones.reunion_confirmado_participante')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values, )

    # cambio al estado terminado
    def action_set_done(self):
        """ cierra registro """
        self.write({'state': 'done'})

    # cambio al estado cancelado
    def action_cancel(self):
        self.write({'state': 'cancel'})
        # envió la notificación a los seguidores
        self.message_post(body='Participación cancelada',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # envío los correo de los seguidores del registro
        for participantes in self.message_partner_ids:
            # envío el correo a los seguidores del registro
            email_values = {'email_to': participantes.email_formatted}
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_reuniones.reunion_cancelado_participante')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True,
                                                           email_values=email_values, )

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ReunionesParticipantes, self).create(vals_list)
        # si auto confirmo asistencia si esta marcada la opción
        if res._check_auto_confirmation():
            res.sudo().action_confirm()

        # creo la lista de seguidores
        participante = res['name']
        # agrego los seguidores al modelo
        res.message_subscribe(partner_ids=participante.partner_id.ids)
        # envió la notificación a los seguidores
        res.message_post(body='Ha sido agregado a una nueva reunión',
                         subtype_xmlid='mail.mt_comment',
                         author_id=self.env.user.partner_id.id)

        # envío el correo a los seguidores del registro
        email_values = {'email_to': participante.email_formatted}
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_app_reuniones.reunion_nuevo_participante')
        template.with_context(local_context).send_mail(res.id, force_send=True,
                                                       email_values=email_values, )
        return res
