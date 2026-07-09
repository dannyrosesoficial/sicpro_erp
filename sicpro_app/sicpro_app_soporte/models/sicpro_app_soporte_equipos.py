# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SoporteEquipos(models.Model):
    _name = 'sicpro.app.soporte.equipos'
    _description = 'Equipos de Soporte'

    name = fields.Char(string='Name', required=True)
    user_ids = fields.Many2many(comodel_name='res.users', string='Miembros')
    active = fields.Boolean(default=True)
    categorias_ids = fields.Many2many(
        comodel_name='sicpro.app.soporte.categoria', string='Categoria')
    company_id = fields.Many2one(
        'res.company', string="Proceso", default=lambda self: self.env[
            'res.company']._company_default_get('sicpro.app.soporte'))
    color = fields.Integer("Color Index", default=0)
    ticket_ids = fields.One2many('sicpro.app.soporte', 'team_id',
                                 string="Tickets")
    todo_ticket_ids = fields.One2many('sicpro.app.soporte', 'team_id',
                                      string="Todo tickets")
    todo_ticket_count = fields.Integer(string="Number of tickets",
                                       compute='_compute_todo_tickets')
    todo_ticket_count_unassigned = fields.Integer(
        string="Number of tickets unassigned", compute='_compute_todo_tickets')
    todo_ticket_count_unattended = fields.Integer(
        string="Number of tickets unattended", compute='_compute_todo_tickets')
    todo_ticket_count_high_priority = fields.Integer(
        string="Number of tickets in high priority",
        compute='_compute_todo_tickets')

    @api.depends('ticket_ids', 'ticket_ids.stage_id')
    def _compute_todo_tickets(self):
        for record in self:
            record.todo_ticket_ids = record.ticket_ids.filtered(
                lambda ticket: not ticket.closed)
            record.todo_ticket_count = len(record.todo_ticket_ids)
            record.todo_ticket_count_unassigned = len(
                record.todo_ticket_ids.filtered(
                    lambda ticket: not ticket.user_id))
            record.todo_ticket_count_unattended = len(
                record.todo_ticket_ids.filtered(
                    lambda ticket: ticket.unattended))
            record.todo_ticket_count_high_priority = len(
                record.todo_ticket_ids.filtered(
                    lambda ticket: ticket.priority == '3'))
