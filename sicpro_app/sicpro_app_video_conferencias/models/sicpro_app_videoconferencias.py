# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from random import choice
import pytz


def create_hash():
    size = 32
    values = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    p = ''
    p = p.join([choice(values) for i in range(size)])
    return p


class JistiMeet(models.Model):
    _name = 'sicpro.app.videoconferencias'
    _description = 'Gestor de VideoConferencias'
    _order = 'date desc'

    def _get_default_participant(self):
        result = []
        result.append(self.env.user.id)
        return [(6, 0, result)]

    name = fields.Char('Nombre de la Sala', required=True)
    hash = fields.Char('Hash')
    date = fields.Datetime('Fecha', required=True)
    date_delay = fields.Float('Duración', required=True, default=1.0)
    participants = fields.Many2many('res.users', string='Organizador', required=True, default=_get_default_participant)
    external_participants = fields.One2many('sicpro.app.videoconferencias.usuarioexterno', 'meet', string='Participantes Externos')
    url = fields.Char(string='URL de la Sala', compute='_compute_url')
    closed = fields.Boolean('Closed', default=False)
    current_user = fields.Many2one('res.users', compute='_get_current_user')

    @api.depends()
    def _get_current_user(self):
        for rec in self:
            rec.current_user = self.env.user

    @api.model
    def create(self, vals):
        vals['hash'] = create_hash()
        res = super(JistiMeet, self).create(vals)
        return res

    def action_close_meeting(self):
        self.write({'closed': True})

    def action_reopen_meeting(self):
        self.write({'closed': False})

    def open(self):
        return {'name': 'VideoConferencia',
                'res_model': 'ir.actions.act_url',
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': self.url
                }

    @api.model
    def _compute_url(self):
        config_url = self.env['ir.config_parameter'].sudo().get_param(
            'sicpro_app_video_conferencias.jitsi_meet_url',
            default='https://jitsi.etecsa.cu/')
        for r in self:
            if r.hash and r.name:
                r.url = config_url + r.hash


class JitsiMeetExternalParticipant(models.Model):
    _name = 'sicpro.app.videoconferencias.usuarioexterno'
    _description = 'Participantes externos para la VideoConferencia'
    _order = 'name'

    name = fields.Char('Correo')
    usuario = fields.Many2one('res.users', string='Usuario')
    meet = fields.Many2one('sicpro.app.videoconferencias', string='Sala')
    partner_id = fields.Many2one(related='meet.create_uid.partner_id')
    meeting_date = fields.Datetime(related='meet.date',
                                   string='Fecha de la Videoconferencia')
    meeting_name = fields.Char(related='meet.name', string='Nombre de la Sala')
    meeting_url = fields.Char(related='meet.url',string='Url de la Sala')
    send_mail = fields.Boolean('Enviar', default=True)
    mail_sent = fields.Boolean('Enviado', readonly=True, default=False)
    date_formated = fields.Char(compute='_format_date')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [('name_uniq', 'unique (usuario, meet)',
                         "El nombre del usuario o correo ya existe!"), ]


    @api.onchange('usuario')
    def _onchange_usuario(self):
        if self.usuario:
            self.name = self.usuario.email

    def _format_date(self):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        for part in self:
            part.date_formated = datetime.strftime(
                pytz.utc.localize(part.meeting_date).astimezone(local),
                "%d/%m/%Y, %H:%M:%S")

    @api.model
    def create(self, vals):
        res = super(JitsiMeetExternalParticipant, self).create(vals)
        if res.send_mail:
            template = self.env.ref('sicpro_app_video_conferencias.email_template_edi_jitsi_meet')
            self.env['mail.template'].sudo().browse(template.id).send_mail(res.id)
            res.sudo().write({'mail_sent': True})
        return res

    def write(self, vals):
        if 'send_mail' in vals and vals.get('send_mail'):
            if not self.mail_sent:
                template = self.env.ref('sicpro_app_video_conferencias.email_template_edi_jitsi_meet')
                self.env['mail.template'].sudo().browse(template.id).send_mail(self.id)
                vals.update({'mail_sent': True})
        return super(JitsiMeetExternalParticipant, self).write(vals)
