# -*- coding: utf-8 -*-


from random import randint

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class SoporteTicket(models.Model):
    _name = 'sicpro.app.soporte'
    _description = 'Soporte de Ayuda'
    # _rec_name = 'number'
    _order = 'number desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_stage_id(self):
        return self.env['sicpro.app.soporte.estados'].search([], limit=1).id

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    number = fields.Char(string='# Ticket', default="/", readonly=True)
    name = fields.Char(string='Titulo', required=True)
    descripcion = fields.Text(string='Descripción', required=True)
    user_ids = fields.Many2many(comodel_name='res.users', related='team_id.user_ids', string='Usuarios')
    user_id = fields.Many2one('res.users', string='Asignado a', tracking=True, domain="[('id','in',user_ids)]")
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
    stage_id = fields.Many2one('sicpro.app.soporte.estados', string='Estado', group_expand='_read_group_stage_ids',
                               default=_get_default_stage_id)
    partner_user_id = fields.Many2one('res.users', string='Solicitante', index=True, required=True,
                                      default=lambda self: self.env.uid)
    partner_id = fields.Many2one('res.partner', string='Usuario relacionado', related='partner_user_id.partner_id',
                                 store=True)
    partner_name = fields.Char(string='Solicitado por', related='partner_id.name', store=True)
    partner_email = fields.Char(string='Correo', related='partner_id.email', store=True)
    fecha_ticket = fields.Datetime(string='Creado', default=fields.Datetime.now, )
    last_stage_update = fields.Datetime(string='Última actualización', default=fields.Datetime.now, )
    assigned_date = fields.Datetime(string='Fecha Asignado')
    closed_date = fields.Datetime(string='Fecha Terminado')
    closed = fields.Boolean(related='stage_id.closed', store=True)
    unattended = fields.Boolean(related='stage_id.unattended', store=True)
    tag_ids = fields.Many2many('sicpro.app.soporte.etiquetas', string='Etiquetas')
    company_id = fields.Many2one('res.company', string='Proceso', required=True, readonly=True,
                                 default=lambda self: self.env.company)
    channel_id = fields.Many2one('sicpro.app.soporte.canales', string='Vía de solicitud')
    team_id = fields.Many2one('sicpro.app.soporte.equipos', string='Equipos')
    team_id_bitacora = fields.Boolean(string='Equipo Bitácora', related='team_id.bitacora', store=True)
    team_id_commits = fields.Boolean(string='No mostrar commits', related='team_id.commits', store=True)
    bitacora = fields.Many2one(comodel_name='sicpro.app.soporte.bitacora', string='Bitácora', required=False)
    priority = fields.Selection(selection=[('0', _('Baja')), ('1', _('Media')), ('2', _('Alta')), ('3', _('Muy Alta')),],
                                string='Prioridad', default='1')
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    kanban_state = fields.Selection(
        [('normal', 'Normal'), ('done', 'Listo para siguiente estado'), ('blocked', 'Bloqueado')],
        string='Estado Kanban', default='normal')
    active = fields.Boolean('Active', default=True)
    version_id = fields.Many2one(comodel_name='sicpro.app.soporte.versiones', string='Versión', required=False,
                                 domain="[('stage_id.inicial','=',True)]")
    aplicaciones = fields.Many2one( comodel_name='sicpro.app.soporte.aplicaciones', string='Aplicación',
                                    domain="[('stage_id.descontinuado','=', False)]", required=False)
    grupo_ejecutor = fields.Boolean(string='grupo_ejecutor', compute='_compute_grupo_ejecutor',
                                    default=lambda self: self._compute_grupo_ejecutor())
    grupo_responsable = fields.Boolean(string='grupo_responsable', compute='_compute_grupo_responsable',
                                       default=lambda self: self._compute_grupo_responsable())
    asignado = fields.Boolean(string='Asignado', required=False)
    dias_pendientes = fields.Char(string='Dias_pendientes', compute="_compute_dias_pendientes")
    tareas_ids = fields.One2many('sicpro.app.soporte.tareas', 'ticket_id', string='Tareas', )
    cantidad_tareas = fields.Integer("Número de Tareas", compute='_compute_cantidad_horas')
    cantidad_horas_tareas = fields.Float("Total de Horas", compute='_compute_cantidad_horas')
    total_dias_tareas = fields.Float("Total de días", digits=(12, 0), compute='_compute_cantidad_horas')
    horas_planificadas = fields.Float(string='Horas Planificadas')
    progreso = fields.Float(string='Progreso', compute="_compute_progreso")
    # Identifico si el usuario pertenece al grupo de permisos especificado
    group_soporte_usuario = fields.Boolean(compute="_compute_is_group_data", )

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['sicpro.app.soporte.estados'].search([])
        return stage_ids

    # calcula él por ciento de avance de las tareas
    def _compute_progreso(self):
        if self.horas_planificadas != 0 and self.cantidad_horas_tareas != 0:
            self.progreso = round(
                (self.cantidad_horas_tareas / self.horas_planificadas) * 100, 2)
        else:
            self.progreso = 0
            # acción del botón tareas

    # no hace ninguna función
    def action_empaty_tareas(self, ):
        action = None

    # calcula el total de días de las tareas y la cantidad de horas
    def _compute_cantidad_horas(self):
        horas = 7
        for item in self:
            # cuenta la cantidad de tareas del ticket
            item.cantidad_tareas = len(item.tareas_ids)
            # suma la cantidad de horas total de las tareas
            item.cantidad_horas_tareas = round(
                sum(item.tareas_ids.mapped('horas')), 2)
            # calcula el total de días de las tareas
            item.total_dias_tareas = round(
                sum(item.tareas_ids.mapped('horas')), 2) / horas

    # calcular los días pendientes
    def _compute_dias_pendientes(self):
        hoy = fields.Date.context_today(self)
        for item in self:
            dias = abs(hoy - item.fecha_ticket.date()).days
            item.dias_pendientes = str(dias) + " días de iniciado"

    # verifica que el usuario activo pertenezca al grupo Responsable
    def _compute_grupo_responsable(self):
        resp = self.env['res.users'].has_group(
            'sicpro_app_soporte.group_soporte_responsable')
        self.grupo_responsable = resp
        return resp

    # verífica que el usuario activo pertenezca al grupo ejecutor
    def _compute_grupo_ejecutor(self):
        ejec = self.env['res.users'].has_group(
            'sicpro_app_soporte.group_soporte_ejecutor')
        self.grupo_ejecutor = ejec
        return ejec

    @api.constrains('version_id', 'aplicaciones')
    def _crear_relacion_version_ticket(self):
        self.ensure_one()
        # actualizo el ticket en la versión de desarrollo
        if self.version_id:
            ticket = self._origin.id
            version = self.version_id.id
            self.env['sicpro.app.soporte.versiones'].search(
                [('id', '=', version)]).write({'tickets_ids': [(None, ticket)], })

            # actualizo la aplicación en la versión de desarrollo
            if self.aplicaciones:
                app = self.aplicaciones.id
                # busco la aplicación y la paso al estado de desarrollo
                desarrollo = self.env['sicpro.app.soporte.estados.aplicaciones'].search([('desarrollo', '=', True)]).id
                self.env['sicpro.app.soporte.aplicaciones'].search([('id', '=', app)]).write({'stage_id': desarrollo, })
                # agrego la aplicación al trabajo en la versión
                self.env['sicpro.app.soporte.versiones'].search([('id', '=', version)]).write(
                    {'aplicaciones_ids': [(4, app)], })

    # asignarme la tarea específica
    def asignarme_la_tarea(self):
        self.write({'kanban_state': 'done', 'user_id': self.env.user.id})
        # agrego los seguidores al modelo
        self.sudo().message_subscribe(partner_ids=self.user_id.partner_id.ids)
        # envío la notificación al ejecutor
        self.sudo().message_post(body='Ticket asignado', subtype_xmlid='mail.mt_comment',
                                 author_id=self.env.user.partner_id.id)
        # envío el correo electrónico
        participantes = self.user_id.email_formatted
        email_values = {'email_to': participantes}
        template = self.env.ref('sicpro_app_soporte.soporte_ticket_asignado')
        template.send_mail(self.id, force_send=True, email_values=email_values, )
        self.asignado = True

    # asignar la tarea al ejecutor
    def asignar_al_ejecutor(self):
        if not self.user_id:
            raise ValidationError(_('¡Tienes que seleccionar un ejecutor para el ticket!!'))
        else:
            self.write({'kanban_state': 'done'})
            # agrego los seguidores al modelo
            self.sudo().message_subscribe(partner_ids=self.user_id.partner_id.ids)
            # envío la notificación al ejecutor
            self.sudo().message_post(body='Ticket asignado', subtype_xmlid='mail.mt_comment',
                                     author_id=self.env.user.partner_id.id)
            # envío el correo electrónico
            participantes = self.user_id.email_formatted
            email_values = {'email_to': participantes}
            template = self.env.ref('sicpro_app_soporte.soporte_ticket_asignado')
            template.send_mail(self.id, force_send=True, email_values=email_values, )
            self.asignado = True

    @api.model
    def create(self, vals):
        res = super(SoporteTicket, self).create(vals)
        if vals.get('number', '/') == '/':
            seq = self.env['ir.sequence']
            if 'company_id' in vals:
                seq = seq.with_context(force_company=vals['company_id'])
            res['number'] = seq.next_by_code('sicpro.app.soporte.sequence') or '/'

        # Crear un duplicado del ticket en la tabla de todos los tickets
        res.env['sicpro.app.soporte.todos'].sudo().create({'ticket': res._origin.id})

        # busco al responsable de la distribución
        responsable = self.env.ref('sicpro_app_soporte.group_soporte_responsable').users
        # agrego los seguidores al modelo
        res.sudo().message_subscribe(partner_ids=responsable.partner_id.ids)
        # envió la notificación a los seguidores
        res.sudo().message_post(body='Ticket creado', subtype_xmlid='mail.mt_comment',
                                author_id=self.env.user.partner_id.id)

        # Selecciono el usuario y los administradores
        notifica = ''
        for value in responsable:
            notifica += str(value.email_formatted)
        notifica += str(res['partner_user_id'].email_formatted)

        email_values = {'email_to': notifica, }
        # envío el correo electrónico
        template = self.env.ref('sicpro_app_soporte.soporte_ticket_nuevo')
        template.send_mail(res.id, force_send=True, email_values=email_values, )
        return res

    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if "number" not in default:
            default['number'] = self.env['ir.sequence'].next_by_code(
                'sicpro.app.soporte.sequence') or '/'
        res = super(SoporteTicket, self).copy(default)
        return res

    # es sobres escrito por el módulo de: sicpro_modulo_api_conector_gitlab_soporte
    def write(self, vals):
        res = super(SoporteTicket, self).write(vals)
        for ticket in self:
            now = fields.Datetime.now()
            if vals.get('stage_id'):
                stage_obj = self.env['sicpro.app.soporte.estados'].browse(
                    [vals['stage_id']])
                ticket['last_stage_update'] = now
                if stage_obj.closed:
                    if ticket['aplicaciones'] and ticket['version_id']:
                        ticket['closed_date'] = now
                        # envió la notificación a los seguidores
                        ticket.message_post(body='Ticket cerrado', subtype_xmlid='mail.mt_comment',
                                            author_id=self.env.user.partner_id.id)
                        for participante in ticket.message_partner_ids:
                            # envío el correo electrónico
                            email_values = {'email_to': participante.email_formatted}
                            template = self.env.ref('sicpro_app_soporte.soporte_ticket_cambio_estado')
                            template.send_mail(ticket.id, force_send=True, email_values=email_values, )
                    else:
                        raise ValidationError(_("Campos no válidos: Verifique el campo de Aplicación o de Versión. "
                                                "Si cree que es un error contacte al administrador"))

            if vals.get('user_id'):
                ticket['assigned_date'] = now

        if vals.get('partner_id'):
            self.message_subscribe([vals['partner_id']])
        return res

    @api.model
    def _compute_is_group_data(self):
        self.group_soporte_usuario = self.env['res.users'].has_group(
            'module_name.group_id_xml')
