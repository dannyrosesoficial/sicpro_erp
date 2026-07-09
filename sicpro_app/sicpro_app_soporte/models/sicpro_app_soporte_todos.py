# -*- coding: utf-8 -*-


from odoo import api, fields, models


class SoporteTicketTodos(models.Model):
    _name = 'sicpro.app.soporte.todos'
    _description = 'Todos los Tickets de Soporte de Ayuda'
    _rec_name = 'number'
    _order = 'number desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_stage_id(self):
        return self.env['sicpro.app.soporte.estados'].search([], limit=1).id

    ticket = fields.Many2one(comodel_name='sicpro.app.soporte')
    number = fields.Char(string='# Ticket', related='ticket.number', store=True)
    name = fields.Char(string='Titulo', related='ticket.name', store=True)
    descripcion = fields.Text(string='Descripción', related='ticket.descripcion', store=True)
    user_id = fields.Many2one('res.users', related='ticket.user_id', store=True)
    stage_id = fields.Many2one('sicpro.app.soporte.estados', string='Estado',
                               related='ticket.stage_id', store=True, group_expand='_read_group_stage_ids',)
    partner_user_id = fields.Many2one('res.users', related='ticket.partner_user_id', store=True)
    partner_id = fields.Many2one('res.partner', string='Usuario relacionado', related='ticket.partner_id', store=True)
    partner_name = fields.Char(string='Solicitado por', related='ticket.partner_name', store=True)
    partner_email = fields.Char(string='Correo', related='ticket.partner_email', store=True)
    fecha_ticket = fields.Datetime(string='Creado', related='ticket.fecha_ticket', store=True)
    last_stage_update = fields.Datetime(string='Última actualización de estado', related='ticket.last_stage_update',
                                        store=True)
    assigned_date = fields.Datetime(string='Fecha Asignado', related='ticket.assigned_date', store=True)
    closed_date = fields.Datetime(string='Fecha Terminado', related='ticket.closed_date', store=True)
    closed = fields.Boolean(related='ticket.closed', store=True)
    unattended = fields.Boolean(related='ticket.unattended', store=True)
    company_id = fields.Many2one('res.company', string='Proceso', related='ticket.company_id', store=True)
    channel_id = fields.Many2one('sicpro.app.soporte.canales', string='Vía solicitud',
                                 related='ticket.channel_id', store=True)
    team_id = fields.Many2one('sicpro.app.soporte.equipos', string='Equipos', related='ticket.team_id', store=True)
    user_ids = fields.Many2many(comodel_name='res.users', related='team_id.user_ids', string='Usuarios')
    priority = fields.Selection(string='Prioridad', related='ticket.priority', store=True)
    horas_planificadas = fields.Float(string='Horas Planificadas', related='ticket.horas_planificadas', store=True)
    color = fields.Integer(string='Color', related='ticket.color', store=True)
    kanban_state = fields.Selection(string='Estado Kanban', related='ticket.kanban_state', store=True)
    active = fields.Boolean('Active', related='ticket.active', store=True)
    version_id = fields.Many2one(comodel_name='sicpro.app.soporte.versiones',
                                 string='Versión', related='ticket.version_id', store=True)
    aplicaciones = fields.Many2one(comodel_name='sicpro.app.soporte.aplicaciones', string='Aplicación',
                                   related='ticket.aplicaciones', store=True)
    grupo_ejecutor = fields.Boolean(string='grupo_ejecutor', related='ticket.grupo_ejecutor', store=True)
    grupo_responsable = fields.Boolean(string='grupo_responsable', related='ticket.grupo_responsable', store=True)
    tareas_ids = fields.One2many('sicpro.app.soporte.tareas', 'ticket_id', string='Tareas',
                                 related='ticket.tareas_ids', store=True)
    asignado = fields.Boolean(string='Asignado', related='ticket.asignado', store=True)
    cantidad_tareas = fields.Integer("Número de Tareas", compute='_compute_cantidad_horas')
    cantidad_horas_tareas = fields.Float("Total de Horas", compute='_compute_cantidad_horas')
    total_dias_tareas = fields.Float("Total de días", digits=(12, 0), compute='_compute_cantidad_horas')
    dias_pendientes = fields.Char(string='Dias_pendientes', compute="_compute_dias_pendientes")
    progreso = fields.Float(string='Progreso', compute="_compute_progreso")

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['sicpro.app.soporte.estados'].search([])
        return stage_ids

    def _compute_progreso(self):
        if self.horas_planificadas != 0 and self.cantidad_horas_tareas != 0:
            self.progreso = round(
                (self.cantidad_horas_tareas / self.horas_planificadas) * 100, 2)
        else:
            self.progreso = 0
            # acción del botón tareas

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