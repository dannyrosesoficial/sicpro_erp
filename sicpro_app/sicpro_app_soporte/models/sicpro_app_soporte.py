# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools


class SoporteTicket(models.Model):
    _name = 'sicpro.app.soporte'
    _descripcion = 'Soporte Ticket'
    _rec_name = 'number'
    _order = 'number desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_stage_id(self):
        return self.env['sicpro.app.soporte.estados'].search([], limit=1).id

    number = fields.Char(string='# Ticket', default="/", readonly=True)
    name = fields.Char(string='Titulo', required=True)
    descripcion = fields.Text(string='Descripción', required=True)
    user_id = fields.Many2one(
        'res.users', string='Asignado a', tracking=True,
        domain=lambda self: [('groups_id', 'in',
                              self.env.ref(
                                  'sicpro_app_soporte.group_soporte_ejecutor').id)])

    user_ids = fields.Many2many(comodel_name='res.users',
                                related='team_id.user_ids', string='Usuarios')

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['sicpro.app.soporte.estados'].search([])
        return stage_ids

    stage_id = fields.Many2one('sicpro.app.soporte.estados', string='Estado',
                               group_expand='_read_group_stage_ids',
                               default=_get_default_stage_id,
                               track_visibility='onchange', )
    partner_id = fields.Many2one('res.partner')
    partner_name = fields.Char()
    partner_email = fields.Char()
    create_date = fields.Datetime(string='Creado',
                                  default=fields.Datetime.now, )
    last_stage_update = fields.Datetime(
        string='Última actualización de estado', default=fields.Datetime.now,
    )
    assigned_date = fields.Datetime(string='Fecha Asignado')
    closed_date = fields.Datetime(string='Fecha Terminado')
    closed = fields.Boolean(related='stage_id.closed')
    unattended = fields.Boolean(related='stage_id.unattended')
    tag_ids = fields.Many2many('sicpro.app.soporte.etiquetas',
                               string='Etiquetas')
    company_id = fields.Many2one('res.company', string="Proceso",
                                 default=lambda self: self.env[
                                     'res.company']._company_default_get(
                                     'sicpro.app.soporte')
                                 )
    channel_id = fields.Many2one('sicpro.app.soporte.canales',
                                 string='Canal',
                                 help='Channel indicates where the source of a ticket'
                                      'comes from (it could be a phone call, an email...)', )
    category_id = fields.Many2one('sicpro.app.soporte.categoria',
                                  string='Categoría')
    team_id = fields.Many2one('sicpro.app.soporte.equipos')
    priority = fields.Selection(selection=[
        ('0', _('Low')),
        ('1', _('Medium')),
        ('2', _('High')),
        ('3', _('Very High')),
    ], string='Prioridad', default='1')
    attachment_ids = fields.One2many('ir.attachment', 'res_id',
                                     domain=[('res_model', '=',
                                              'sicpro.app.soporte')],
                                     string="Archivos Adjuntos")
    color = fields.Integer(string='Color Index')
    kanban_state = fields.Selection([
        ('normal', 'Default'),
        ('done', 'Ready for next stage'),
        ('blocked', 'Blocked')], string='Estado Kanban')
    active = fields.Boolean('Active', default=True)

    def assign_to_me(self):
        self.write({'user_id': self.env.user.id})

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.partner_name = self.partner_id.name
            self.partner_email = self.partner_id.email

    # @api.onchange('team_id', 'user_id')
    # def _onchange_dominion_user_id(self):
    # if self.user_id:
    #   if self.user_id and self.user_ids and \
    #          self.user_id not in self.user_ids:
    #     self.update({
    #        'user_id': False
    #   })
    #  return {'domain': {'user_id': []}}
    # if self.team_id:
    #   return {'domain': {'user_id': [('id', 'in', self.user_ids.ids)]}}
    # else:
    #   return {'domain': {'user_id': []}}

    # ---------------------------------------------------
    # CRUD
    # ---------------------------------------------------

    @api.model
    def create(self, vals):
        if vals.get('number', '/') == '/':
            seq = self.env['ir.sequence']
            if 'company_id' in vals:
                seq = seq.with_context(force_company=vals['company_id'])
            vals['number'] = seq.next_by_code(
                'sicpro.app.soporte.sequence') or '/'
        # res = super().create(vals)

        # context: no_log, because subtype already handle this
        tickets = super(SoporteTicket, self).create(vals)
        for ticket in tickets:
            if ticket.partner_id:
                ticket.message_subscribe(partner_ids=ticket.partner_id.ids)
        # make customer follower
        # for ticket in tickets:
        # if ticket.partner_id:
        # ticket.message_subscribe(partner_ids=ticket.partner_id.ids)

        return tickets

    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if "number" not in default:
            default['number'] = self.env['ir.sequence'].next_by_code(
                'sicpro.app.soporte.sequence'
            ) or '/'
        res = super(SoporteTicket, self).copy(default)
        return res

    def write(self, vals):
        for ticket in self:
            now = fields.Datetime.now()
            if vals.get('stage_id'):
                stage_obj = self.env['sicpro.app.soporte.estados'].browse(
                    [vals['stage_id']])
                vals['last_stage_update'] = now
                if stage_obj.closed:
                    vals['closed_date'] = now
            if vals.get('user_id'):
                vals['assigned_date'] = now

        res = super(SoporteTicket, self).write(vals)

        if vals.get('partner_id'):
            self.message_subscribe([vals['partner_id']])

        return res

    # ---------------------------------------------------
    # Mail gateway
    # ---------------------------------------------------

    def _track_template(self, changes):
        res = super(SoporteTicket, self)._track_template(changes)
        test_task = self[0]
        # changes, tracking_value = tracking[test_task.id]
        if "stage_id" in changes and test_task.stage_id.mail_template_id:
            res['stage_id'] = (test_task.stage_id.mail_template_id,
                               {"composition_mode": "mass_mail"})

        return res

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Override message_new from mail gateway so we can set correct
        default values.
        """
        if custom_values is None:
            custom_values = {}
        defaults = {
            'name': msg.get('subject') or _("No Subject"),
            'descripcion': msg.get('body'),
            'partner_email': msg.get('from'),
            'partner_id': msg.get('author_id')
        }
        defaults.update(custom_values)

        # Write default values coming from msg
        ticket = super().message_new(msg, custom_values=defaults)

        # Use mail gateway tools to search for partners to subscribe
        email_list = tools.email_split(
            (msg.get('to') or '') + ',' + (msg.get('cc') or '')
        )
        partner_ids = [p for p in ticket._find_partner_from_emails(
            email_list, force_create=False
        ) if p]
        ticket.message_subscribe(partner_ids)

        return ticket

    def message_update(self, msg, update_vals=None):
        """ Override message_update to subscribe partners """
        email_list = tools.email_split(
            (msg.get('to') or '') + ',' + (msg.get('cc') or '')
        )
        partner_ids = [p for p in self._find_partner_from_emails(
            email_list, force_create=False
        ) if p]
        self.message_subscribe(partner_ids)
        return super().message_update(msg, update_vals=update_vals)

    def message_get_suggested_recipients(self):
        recipients = super().message_get_suggested_recipients()

        for ticket in self:
            reason = _('Partner Email') \
                if ticket.partner_id and ticket.partner_id.email \
                else _('Partner Id')

            if ticket.partner_id and ticket.partner_id.email:
                ticket._message_add_suggested_recipient(
                    recipients,
                    partner=ticket.partner_id,
                    reason=reason
                )
            elif ticket.partner_email:
                ticket._message_add_suggested_recipient(
                    recipients,
                    email=ticket.partner_email,
                    reason=reason
                )
        return recipients
