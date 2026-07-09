# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class SoporteTicketTareas(models.Model):
    _name = 'sicpro.app.soporte.tareas'
    _description = 'Tareas de Soporte de Ayuda'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre', required=True)
    user_id = fields.Many2one('res.users', string='Asignado a',
                              default=lambda self: self.env.uid)
    descripcion = fields.Text(string='Descripción', required=True)
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    estado = fields.Selection(
        [('pendiente', 'Pendiente'), ('proceso', 'En Proceso'),
         ('bloqueado', 'Bloqueado'), ('cumplido', 'Cumplido')],
        string='Estado', default='pendiente')
    active = fields.Boolean(string='Activo', default=True, index=True)
    ticket_id = fields.Many2one('sicpro.app.soporte', required=False,
                                index=True)
    horas = fields.Float(string='Horas de Trabajo', required=True)
