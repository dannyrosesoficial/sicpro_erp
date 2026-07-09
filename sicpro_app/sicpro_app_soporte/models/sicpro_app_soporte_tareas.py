# -*- coding: utf-8 -*-


from odoo import _, api, fields, models, tools
from random import randint
from datetime import datetime
import pytz
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class SoporteTicketTareas(models.Model):
    _name = 'sicpro.app.soporte.tareas'
    _description = 'Tareas de Soporte de Ayuda'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo \
            as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.\
                NucleoReadonly.nucleo_readonly_check(self)

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
    active = fields.Boolean('Active', default=True)
    ticket_id = fields.Many2one('sicpro.app.soporte', required=False,
                                index=True)
    horas = fields.Float(string='Horas de Trabajo', required=True)

