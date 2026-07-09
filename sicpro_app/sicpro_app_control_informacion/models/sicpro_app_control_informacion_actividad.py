# -*- coding: utf-8 -*-
from datetime import datetime
from random import randint

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class ControlInformacionActividades(models.Model):
    _name = 'sicpro.app.control.informacion.actividad'
    _description = 'Actividades para el control de información'

    name = fields.Char('Actividad', required=True)
    descripcion = fields.Char(string="Descripción de la actividad", required=True)
    active = fields.Boolean('Activo', default=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    gestores = fields.Many2many('res.users', 'gestores_control_informacion_rel', string='Gestores', required=True)
    areas = fields.Many2many('sicpro.app.control.informacion.areas', 'areas_control_informacion_rel', string='Áreas',
                             required=True)
    dia_entrega = fields.Integer('Día de entregas', required=True, default=0)
    notificar = fields.Many2many('sicpro.app.control.informacion.dias', 'notificar_control_informacion_rel',
                                 'actividades_id', 'dias_id', string='Notificaciones(días)', required=False)
    cuenta_mes_actual = fields.Integer(string="Cantidad del mes actual", compute='_compute_todo_control')
    cuenta_enviados = fields.Integer(string="Cantidad enviados", compute='_compute_todo_control')
    cuenta_pendientes = fields.Integer(string="Cantidad pendiente", compute='_compute_todo_control')
    cuenta_validados = fields.Integer(string="Cantidad validada", compute='_compute_todo_control')
    cuenta_atrasados = fields.Integer(string="Cantidad de atrasado", compute='_compute_todo_control')

    # cuenta los controles por actividad para el dashboard
    @api.model
    def _compute_todo_control(self):
        # busco el mes actual
        nombre_mes = self.env['sicpro.nomenclador.meses'].search(
            ['&', ('active', '=', True), ('codigo_mes', '=', datetime.today().month)])
        mes_actual = nombre_mes.name
        # busco el año actual
        anio_actual = datetime.today().strftime("%Y")

        for item in self:
            # cuenta los controles del mes
            item.cuenta_mes_actual = self.env['sicpro.app.control.informacion.control.actividades'].search_count(
                ['&', '&', ('name', '=', item.id), ('mes', '=', mes_actual), ('anio', '=', anio_actual)])
            # cuenta los controles enviados
            item.cuenta_enviados = self.env['sicpro.app.control.informacion.control.actividades'].search_count(
                ['&', ('name', '=', item.id), ('estado', '=', 'enviado')])
            # cuenta los controles pendientes
            item.cuenta_pendientes = self.env['sicpro.app.control.informacion.control.actividades'].search_count(
                ['&', ('name', '=', item.id), ('estado', '=', 'pendiente')])
            # cuenta los controles validados
            item.cuenta_validados = self.env['sicpro.app.control.informacion.control.actividades'].search_count(
                ['&', ('name', '=', item.id), ('estado', '=', 'validado')])
            # cuenta los controles atrasados
            item.cuenta_atrasados = self.env['sicpro.app.control.informacion.control.actividades'].search_count(
                ['&', ('name', '=', item.id), ('estado', '=', 'atrasado')])

    # chequea que los días de entrega esten entre el 1 y 30 de cada mes
    @api.constrains('dia_entrega')
    def _check_dia_entrega(self):
        for item in self:
            if item.dia_entrega < 1 or item.dia_entrega > 30:
                raise ValidationError(_('Los días de entrega no puede ser anterior a 1 o superior a 30.'))
