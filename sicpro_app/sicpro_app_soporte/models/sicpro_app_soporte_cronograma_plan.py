# -*- coding: utf-8 -*-

import json
from datetime import timedelta
from random import randint

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class SoporteCronogramaPlan(models.Model):
    _name = 'sicpro.app.soporte.cronograma.plan'
    _description = 'Cronograma Planificado para el Desarrollo'
    _order = "id"

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    anio_id = fields.Many2one(comodel_name='sicpro.app.soporte.cronograma.anio', string='Año', required=True)
    jefe_proyecto = fields.Many2one('res.users', string='Jefe de Proyecto', required=True)
    asignados_proyectos = fields.Many2many('res.users', string='Asignados', required=False)
    descripcion = fields.Html(string='Descripción', required=False)
    fecha_inicio = fields.Date('Fecha de Inicio')
    fecha_fin = fields.Date('Fecha Fin')
    duracion_tarea = fields.Float('Duración', default=7, compute='_compute_planned_duration',
                                  inverse='_inverse_planned_duration', store=True)
    tareas_sucesoras_ids = fields.One2many('sicpro.app.soporte.cronograma.plan.dependencias', 'tarea_id')
    tareas_predecesoras_ids = fields.One2many('sicpro.app.soporte.cronograma.plan.dependencias', 'dependencias_id')
    links_serialized_json = fields.Char('Vínculos JSON serializados', compute="compute_links_json")
    lag_time = fields.Integer('Retraso')
    tareas_predecesoras_recursivas_ids = fields.Many2many(string='Predecesoras Recursivas',
                                                          comodel_name='sicpro.app.soporte.cronograma.plan',
                                                          compute='_compute_tareas_predecesoras_recursivas_ids')
    progress = fields.Integer(string='Progreso')
    progress_percentage = fields.Float(compute='_compute_progress_percentage')

    @api.constrains('name')
    def _check_anio_unico(self):
        uniq = self.env['sicpro.app.soporte.cronograma.anio'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡La tarea introducida existe!. Si cree que es un error contacte al administrador"))

    # calcula el porcentaje de avance
    @api.depends('progress')
    def _compute_progress_percentage(self):
        for u in self:
            u.progress_percentage = u.progress / 100

    # calcula el tiempo de duración de la tarea
    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_planned_duration(self):
        for r in self:
            if r.fecha_inicio and r.fecha_fin:
                elapsed_seconds = (r.fecha_fin - r.fecha_inicio).total_seconds()
                seconds_in_day = 24 * 60 * 60
                r.duracion_tarea = elapsed_seconds / seconds_in_day
                r = r.with_context(ignore_onchange_planned_duration=True)

    # duración de la tarea inversa
    @api.onchange('duracion_tarea', 'fecha_inicio')
    def _inverse_planned_duration(self):
        for r in self:
            if r.fecha_inicio and r.duracion_tarea and not r.env.context.get('ignore_onchange_planned_duration', False):
                r.fecha_fin = r.fecha_inicio + timedelta(days=r.duracion_tarea)

    # busca las tareas predecesoras recursivas
    @api.depends('tareas_predecesoras_ids')
    def _compute_tareas_predecesoras_recursivas_ids(self):
        for item in self:
            item.tareas_predecesoras_recursivas_ids = item.get_dependency_tasks(item, True,)

    # retorna las tareas predecesoras recursivas
    @api.model
    def get_dependency_tasks(self, tarea, recursive=False):
        tareas_predecesoras = tarea.with_context(prefetch_fields=False,).dependency_task_ids
        if recursive:
            for t in tareas_predecesoras:
                tareas_predecesoras |= self.get_dependency_tasks(t, recursive)
        return tareas_predecesoras

    # serializa las tareas en un json
    def compute_links_json(self):
        for r in self:
            links = []
            r.links_serialized_json = '['
            for link in r.tareas_predecesoras_ids:
                json_obj = {
                    'id': link.id,
                    'source': link.tarea_id.id,
                    'target': link.dependencias_id.id,
                    'type': link.tipo_relacion
                }
                links.append(json_obj)
            r.links_serialized_json = json.dumps(links)


class SoporteCronogramaPlanDependencias(models.Model):
    _name = 'sicpro.app.soporte.cronograma.plan.dependencias'
    _description = 'Dependencias de Cronograma Planificado para el Desarrollo'
    _order = "id"

    tarea_id = fields.Many2one('sicpro.app.soporte.cronograma.plan', string='Tarea', required=True)
    anio_id = fields.Many2one('sicpro.app.soporte.cronograma.anio', compute='_compute_anio_id', string='Año')
    dependencias_id = fields.Many2one('sicpro.app.soporte.cronograma.plan', string='Dependencias', required=True)
    tipo_relacion = fields.Selection(
        [("0", "Final a inicio"), ("1", "Inicio a inicio"), ("2", "Final a final"),
         ("3", "Inicio a final")], string='Relación', default="0", required=True)
    state = fields.Selection([('draft', 'Borrador'), ('confirm', 'Confirmar'), ('done', 'Hecho')],
                             string='Estado', default='draft')

    _sql_constraints = [(
        'relacion_tarea_unique', 'unique(tarea_id, dependencias_id)',
        '¡Solo puede existir una relación entre dos tareas!'), ]

    # busca el año de desarrollo perteneciente a la tarea
    @api.onchange('tarea_id', 'dependencias_id')
    def _compute_anio_id(self):
        for r in self:
            if r.tarea_id:
                r.anio_id = r.tarea_id.anio_id
            elif r.dependencias_id:
                r.anio_id = r.dependencias_id.anio_id
