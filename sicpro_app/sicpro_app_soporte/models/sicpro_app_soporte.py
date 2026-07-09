# -*- coding: utf-8 -*-


from odoo import _, api, fields, models, tools
from random import randint
from datetime import datetime
import pytz
from odoo.exceptions import ValidationError


class SoporteTicket(models.Model):
    _name = 'sicpro.app.soporte'
    _description = 'Soporte de Ayuda'
    _rec_name = 'number'
    _order = 'number desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _default_color(self):
        return randint(1, 11)

    def _get_default_stage_id(self):
        return self.env['sicpro.app.soporte.estados'].search([], limit=1).id

    number = fields.Char(string='# Ticket', default="/", readonly=True)
    name = fields.Char(string='Titulo', required=True)
    descripcion = fields.Text(string='Descripción', required=True)
    user_id = fields.Many2one('res.users', string='Asignado a',
        tracking=True, )
    user_ids = fields.Many2many(comodel_name='res.users',
                                related='team_id.user_ids', string='Usuarios')

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['sicpro.app.soporte.estados'].search([])
        return stage_ids

    stage_id = fields.Many2one('sicpro.app.soporte.estados', string='Estado',
                               group_expand='_read_group_stage_ids',
                               default=_get_default_stage_id)

    partner_user_id = fields.Many2one('res.users',
                                      default=lambda self: self.env.uid)
    partner_id = fields.Many2one('res.partner', string='Usuario relacionado',
                                 related='partner_user_id.partner_id',
                                 store=True)
    partner_name = fields.Char(string='Solicitado por',
                               related='partner_id.name', store=True)
    partner_email = fields.Char(string='Correo', related='partner_id.email',
                                store=True)
    fecha_ticket = fields.Datetime(string='Creado',
                                   default=fields.Datetime.now, )
    last_stage_update = fields.Datetime(
        string='Última actualización de estado', default=fields.Datetime.now, )
    assigned_date = fields.Datetime(string='Fecha Asignado')
    closed_date = fields.Datetime(string='Fecha Terminado')
    closed = fields.Boolean(related='stage_id.closed', store=True)
    unattended = fields.Boolean(related='stage_id.unattended', store=True)
    tag_ids = fields.Many2many('sicpro.app.soporte.etiquetas',
                               string='Etiquetas')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True, readonly=True,
                                 default=lambda self: self.env.company)
    channel_id = fields.Many2one('sicpro.app.soporte.canales',
                                 string='Vía solicitud')
    category_id = fields.Many2one('sicpro.app.soporte.categoria',
                                  string='Categoría')
    team_id = fields.Many2one('sicpro.app.soporte.equipos', string='Equipos')
    priority = fields.Selection(
        selection=[('0', _('Low')), ('1', _('Medium')), ('2', _('High')),
            ('3', _('Very High')), ], string='Prioridad', default='1')
    attachment_ids = fields.Many2many('ir.attachment', string="Adjuntos")
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())
    kanban_state = fields.Selection(
        [('normal', 'Normal'), ('done', 'Listo para siguiente estado'),
            ('blocked', 'Bloqueado')], string='Estado Kanban',
        default='normal')
    active = fields.Boolean('Active', default=True)

    version_id = fields.Many2one(comodel_name='sicpro.app.soporte.versiones',
                                 string='Versión', required=False,
                                 domain="[('stage_id.inicial','=',True)]")
    aplicaciones = fields.Many2one(
        comodel_name='sicpro.app.soporte.aplicaciones', string='Aplicación',
        required=False)
    correo_seguidores = fields.Char(string="correo_seguidores", index=True)
    usuario_solicitante = fields.Many2one('res.users',
                                          string='Usuario Solicitante',
                                          default=lambda self: self.env.uid)
    grupo_ejecutor = fields.Boolean(string='grupo_ejecutor',
                                    compute='_compute_grupo_ejecutor')
    grupo_responsable = fields.Boolean(string='grupo_responsable',
                                       compute='_compute_grupo_responsable')
    fecha_ticket_formated = fields.Char(compute='_fecha_ticket_formated')
    asignado = fields.Boolean(string='Asignado', required=False)

    def _fecha_ticket_formated(self):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        for part in self:
            part.fecha_ticket_formated = datetime.strftime(
                pytz.utc.localize(part.fecha_ticket).astimezone(local),
                "%d/%m/%Y, %H:%M:%S")

    # verifica q el usuario activo pertenezca al grupo Responsable
    def _compute_grupo_responsable(self):
        self.grupo_responsable = self.env['res.users'].has_group(
            'sicpro_app_soporte.group_soporte_responsable')

    # verifica q el usuario activo pertenezca al grupo ejecutor
    def _compute_grupo_ejecutor(self):
        self.grupo_ejecutor = self.env['res.users'].has_group(
            'sicpro_app_soporte.group_soporte_ejecutor')

    @api.constrains('version_id')
    def _crear_relacion_version_ticket(self):
        self.ensure_one()
        if self.version_id:
            ticket = self._origin.id
            version = self.version_id.id
            self.env['sicpro.app.soporte.versiones'].search(
                [('id', '=', version)]).write(
                {'tickets_ids': [(None, ticket)], })

    # asignarme la tarea especifica
    def asignarme_la_tarea(self):
        self.write({'kanban_state': 'done', 'user_id': self.env.user.id})
        self.correo_seguidores = self.user_id.email_formatted
        # agrego los seguidores al modelo
        self.sudo().message_subscribe(partner_ids=self.user_id.partner_id.ids)
        # envió la notificación al ejecutor
        self.sudo().message_post(body='Nueva ticket asignado',
                                 message_type='notification',
                                 subtype_xmlid='mail.mt_comment',
                                 author_id=self.env.user.partner_id.id)
        # envío el correo al ejecutor del registro
        template = self.env.ref('sicpro_app_soporte.soporte_ticket_asignado')
        template.send_mail(self.id, force_send=True)

    # asignar la tarea al ejecutor
    def asignar_al_ejecutor(self):
        if not self.user_id:
            raise ValidationError(
                _('Tienes que seleccionar un ejecutor para el ticket !!'))
        else:
            self.write({'kanban_state': 'done'})
            self.correo_seguidores = self.user_id.email_formatted
            # agrego los seguidores al modelo
            self.sudo().message_subscribe(partner_ids=self.user_id.partner_id.ids)
            # envió la notificación al ejecutor
            self.sudo().message_post(body='Nueva ticket asignado',
                                     message_type='notification',
                                     subtype_xmlid='mail.mt_comment',
                                     author_id=self.env.user.partner_id.id)
            # envío el correo al ejecutor del registro
            template = self.env.ref('sicpro_app_soporte.soporte_ticket_asignado')
            template.send_mail(self.id, force_send=True)
            self.asignado = True

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.partner_name = self.partner_id.name
            self.partner_email = self.partner_id.email

    @api.model
    def create(self, vals):
        tickets = super(SoporteTicket, self).create(vals)
        if vals.get('number', '/') == '/':
            seq = self.env['ir.sequence']
            if 'company_id' in vals:
                seq = seq.with_context(force_company=vals['company_id'])
            tickets['number'] = seq.next_by_code(
                'sicpro.app.soporte.sequence') or '/'
        # res = super().create(vals)

        # busco al responsable de la distribución
        responsable = self.env.ref(
            'sicpro_app_soporte.group_soporte_responsable').users

        seguidores = responsable
        # agrego los seguidores al modelo
        tickets.sudo().message_subscribe(partner_ids=seguidores.partner_id.ids)

        # envió la notificación a los seguidores
        tickets.sudo().message_post(body='Nueva ticket creado',
                                    message_type='notification',
                                    subtype_xmlid='mail.mt_comment',
                                    author_id=self.env.user.partner_id.id)
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in seguidores:
            correos = str(correos) + str(follower.email_formatted)
        tickets['correo_seguidores'] = correos
        # envío el correo a los seguidores del registro
        template = self.env.ref('sicpro_app_soporte.soporte_ticket_nuevo')
        template.send_mail(tickets.id, force_send=True)
        return tickets

    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if "number" not in default:
            default['number'] = self.env['ir.sequence'].next_by_code(
                'sicpro.app.soporte.sequence') or '/'
        res = super(SoporteTicket, self).copy(default)
        return res

    def write(self, vals):
        res = super(SoporteTicket, self).write(vals)
        for ticket in self:
            now = fields.Datetime.now()
            if vals.get('stage_id'):
                stage_obj = self.env['sicpro.app.soporte.estados'].browse(
                    [vals['stage_id']])
                vals['last_stage_update'] = now
                if stage_obj.closed:
                    vals['closed_date'] = now
                    # envió la notificación a los seguidores
                    ticket.message_post(body='Ticket cerrado',
                                        message_type='notification',
                                        subtype_xmlid='mail.mt_comment',
                                        author_id=self.env.user.partner_id.id)
                    # mantiene actualizado el correo de los seguidores
                    correos = ''
                    for follower in ticket.message_partner_ids:
                        correos = str(correos) + str(follower.email_formatted)
                    ticket.correo_seguidores = correos
                    # envío el correo a los seguidores del registro
                    template = self.sudo().env.ref(
                        'sicpro_app_soporte.soporte_ticket_cambio_estado')
                    template.send_mail(ticket.id, force_send=True)

            if vals.get('user_id'):
                vals['assigned_date'] = now

        if vals.get('partner_id'):
            self.message_subscribe([vals['partner_id']])

        return res

    # Identifico si el usuario pertenece al grupo de permisos especificado
    group_soporte_usuario = fields.Boolean(compute="_compute_is_group_data", )

    @api.model
    def _compute_is_group_data(self):
        self.group_soporte_usuario = self.env['res.users'].has_group(
            'module_name.group_id_xml')
