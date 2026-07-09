# -*- coding: utf-8 -*-

from odoo import api, fields, models
from random import randint

class MetrologiaDirecciones(models.Model):
    _name = 'sicpro.app.metrologia.direcciones'
    _description = 'Direcciones de equipos de Metrología'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char('Equipo del Proceso', required=True, translate=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())
    request_ids = fields.One2many(
        comodel_name="sicpro.app.metrologia.equipos",
        inverse_name="equipo_mantenimiento_id", copy=False)
    equipment_ids = fields.One2many(
        comodel_name="sicpro.app.metrologia.equipos",
        inverse_name="equipo_mantenimiento_id", copy=False)
    gestores = fields.Many2many(comodel_name='sicpro.app.trabajadores',
                                string='Gestores de Metrología')

    # Para el dashboard
    todo_request_ids = fields.One2many(
        'sicpro.app.metrologia.equipos', string="Requests",
        copy=False, compute='_compute_todo_requests')
    todo_request_count = fields.Integer(string="Número de Equipos",
                                        compute='_compute_todo_requests')
    todo_request_count_laboratorio = fields.Integer(
        string="Cantidad en laboratorio", compute='_compute_todo_requests')
    todo_request_count_sin_calibrar = fields.Integer(
        string="Cantidad sin calibrar", compute='_compute_todo_requests')
    todo_request_count_transferencias = fields.Integer(
        string="Cantidad de Transferencias Pendientes",
        compute='_compute_todo_requests')
    todo_request_planificado = fields.Integer(string="Cantidad Planificada",
                                              compute='_compute_todo_requests')

    @api.depends('request_ids.estado_id.baja',
                 'request_ids.transferencia_pendiente')
    def _compute_todo_requests(self):
        for team in self:
            team.todo_request_ids = team.request_ids.filtered(
                lambda e: e.estado_id.baja == False)
            team.todo_request_count = len(team.todo_request_ids)
            team.todo_request_count_laboratorio = len(
                team.todo_request_ids.filtered(
                    lambda e: e.estado_id.laboratorio == True))
            team.todo_request_count_sin_calibrar = len(
                team.todo_request_ids.filtered(
                    lambda e: e.estado_id.sin_calibrar == True))
            team.todo_request_count_transferencias = len(
                team.todo_request_ids.filtered(
                    lambda e: e.transferencia_pendiente == True))
            team.todo_request_planificado = len(team.todo_request_ids.filtered(
                lambda e: e.aviso_mtto == True))

    @api.depends('equipment_ids')
    def _compute_equipment(self):
        for team in self:
            team.equipment_count = len(team.equipment_ids)
