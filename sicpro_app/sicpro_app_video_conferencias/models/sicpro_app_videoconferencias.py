# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO
import secrets


class JitsiMeet(models.Model):
    _name = 'sicpro.app.videoconferencias'
    _description = 'Gestor de VideoConferencias'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    def _get_default_participant(self):
        return [(6, 0, [self.env.user.id])]

    name = fields.Char(string='Nombre de la Sala', required=True)
    hash = fields.Char(string='Hash', readonly=True, copy=False)
    date = fields.Datetime(string='Fecha', required=True, default=fields.Datetime.now)
    date_delay = fields.Float(string='Duración', required=True, default=1.0)
    participants = fields.Many2many('res.users', string='Organizadores', required=True,
                                    default=_get_default_participant)
    external_participants = fields.One2many('sicpro.app.videoconferencias.usuarioexterno', 'meet',
                                            string='Participantes Externos')
    url = fields.Char(string='URL de la Sala', compute='_compute_url', store=True)
    closed = fields.Boolean(string='Cerrada', default=False, tracking=True)
    current_user = fields.Many2one('res.users', string="current_user", compute='_get_current_user')

    @api.depends()
    def _get_current_user(self):
        for rec in self:
            rec.current_user = self.env.user.id

    @api.depends('hash', 'name')
    def _compute_url(self):
        # Obtenemos la URL base de los parámetros del sistema (Cuba / ETECSA)
        base_url = self.env['ir.config_parameter'].sudo().get_param('sicpro_app_video_conferencias.jitsi_meet_url',
            default='https://jitsi.etecsa.cu/')
        if not base_url.endswith('/'):
            base_url += '/'

        for r in self:
            if r.hash:
                r.url = f"{base_url}{r.hash}"
            else:
                r.url = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('hash'):
                # Generamos un hash único y seguro de 32 caracteres (24 bytes base64)
                vals['hash'] = secrets.token_urlsafe(24)
        return super(JitsiMeet, self).create(vals_list)

    def action_close_meeting(self):
        self.write({'closed': True})

    def action_reopen_meeting(self):
        self.write({'closed': False})

    def open(self):
        self.ensure_one()
        if not self.url:
            raise ValidationError("La URL de la sala no ha sido generada.\n\n" + MSG_SOPORTE_SICPRO)
        return {'type': 'ir.actions.act_url', 'url': self.url, 'target': 'new', }


class JitsiMeetExternalParticipant(models.Model):
    _name = 'sicpro.app.videoconferencias.usuarioexterno'
    _description = 'Participantes externos para la VideoConferencia'
    _order = 'name'

    name = fields.Char(string='Correo')
    usuario = fields.Many2one('res.users', string='Usuario')
    meet = fields.Many2one('sicpro.app.videoconferencias', string='Sala', ondelete='cascade')

    partner_id = fields.Many2one('res.partner', related='meet.create_uid.partner_id', string='Organizador')
    meeting_date = fields.Datetime(related='meet.date', string='Fecha de la Videoconferencia', readonly=True)
    meeting_name = fields.Char(related='meet.name', string='Nombre de la Sala', readonly=True)
    meeting_url = fields.Char(related='meet.url', string='Url de la Sala', readonly=True)

    send_mail = fields.Boolean(string='Enviar Email', default=True)
    mail_sent = fields.Boolean(string='Enviado', readonly=True, default=False)
    company_id = fields.Many2one('res.company', string='Compañía', required=True, default=lambda self: self.env.company)

    @api.constrains('usuario', 'meet')
    def _check_unique_user_meet(self):
        for record in self:
            if record.usuario and record.meet:
                duplicate = self.search(
                    [('usuario', '=', record.usuario.id), ('meet', '=', record.meet.id), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError("¡Registro Duplicado! El usuario %s ya está invitado "
                                            "a esta reunión en SICPRO." % record.usuario.name + MSG_SOPORTE_SICPRO)

    @api.onchange('usuario')
    def _onchange_usuario(self):
        if self.usuario and self.usuario.email:
            self.name = self.usuario.email

    @api.model_create_multi
    def create(self, vals_list):
        records = super(JitsiMeetExternalParticipant, self).create(vals_list)
        template = self.env.ref('sicpro_app_video_conferencias.email_template_edi_jitsi_meet', raise_if_not_found=False)

        for res in records:
            if res.send_mail and template and not res.mail_sent:
                template.sudo().send_mail(res.id, force_send=True)
                res.sudo().write({'mail_sent': True})
        return records

    def write(self, vals):
        # Si se marca 'send_mail' y no se había enviado antes
        if vals.get('send_mail') and not any(self.mapped('mail_sent')):
            template = self.env.ref('sicpro_app_video_conferencias.email_template_edi_jitsi_meet',
                                    raise_if_not_found=False)
            if template:
                for record in self:
                    template.sudo().send_mail(record.id, force_send=True)
                vals['mail_sent'] = True
        return super(JitsiMeetExternalParticipant, self).write(vals)