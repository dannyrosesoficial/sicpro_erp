# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class Preparaciones(models.Model):
    _inherit = "sicpro.app.preparacion.tecnica.preparaciones"

    horas_restantes = fields.Float("Horas restantes",
                                   compute='_compute_horas_restantes',
                                   store=True, readonly=True, )
    horas_dedicadas = fields.Float("Horas dedicadas",
                                   compute='_compute_horas_dedicadas',
                                   compute_sudo=True, store=True, )
    total_horas = fields.Float("Total de Horas",
                               compute='_compute_total_horas',
                               store=True, )
    progreso = fields.Float("Progreso", compute='_compute_progreso_hours',
                            store=True, group_operator="avg", )
    partes_horas_ids = fields.One2many('sicpro.app.partes.horas',
                                       'preparaciones',
                                       'Partes de horas')

    is_start = fields.Boolean(default=False)
    start_date = fields.Datetime()
    end_date = fields.Datetime()

    # inicia el temporizador de actividades
    def start_timer(self):
        self.write({'is_start': True,
                    'start_date': fields.Datetime.now()})

    # termina el temporizador de actividades
    def end_timer(self):
        self.write({'end_date': fields.Datetime.now()})
        ctx = dict(self._context)
        ctx.update({'start_date': self.start_date, 'end_date': self.end_date,
                    'preparaciones_id': self.id})
        view_id = self.env.ref(
            'sicpro_app_partes_horas.sicpro_app_partes_horas_temporizador_views')
        return {
            'view_id': view_id.ids,
            'view_type': 'form',
            "view_mode": 'form',
            'res_model': 'sicpro.app.partes.horas.temporizador',
            'type': 'ir.actions.act_window',
            'context': ctx,
            'target': 'new'
        }

    # suma el total de horas dedicadas en la preparation
    @api.depends('partes_horas_ids.duracion')
    def _compute_horas_dedicadas(self):
        for data in self:
            data.horas_dedicadas = round(
                sum(data.partes_horas_ids.mapped('duracion')), 2)

    # calculo y lleno la ba rra de progreso del parte de horas
    @api.depends('horas_dedicadas', 'horas_planificadas')
    def _compute_progreso_hours(self):
        for data in self:
            if (data.horas_planificadas > 0.0):
                task_total_hours = data.horas_dedicadas
                if task_total_hours > data.horas_planificadas:
                    data.progreso = 100
                else:
                    data.progreso = round(
                        100.0 * task_total_hours / data.horas_planificadas, 2)
            else:
                data.progreso = 0.0

    # calculo las horas restantes para terminar la preparacion
    @api.depends('horas_dedicadas', 'horas_planificadas')
    def _compute_horas_restantes(self):
        for data in self:
            data.horas_restantes = data.horas_planificadas - data.horas_dedicadas

    # calculo el total de horas ejecutadas
    @api.depends('horas_dedicadas', )
    def _compute_total_horas(self):
        for data in self:
            data.total_horas = data.horas_dedicadas
