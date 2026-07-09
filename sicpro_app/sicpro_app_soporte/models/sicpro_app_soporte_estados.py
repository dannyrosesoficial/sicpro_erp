# -*- coding: utf-8 -*-

from odoo import fields, models


class SoporteEstados(models.Model):
    _name = 'sicpro.app.soporte.estados'
    _description = 'Estados del Soporte'
    _order = 'sequence, id'

    name = fields.Char(string='Estado', required=True)
    descripcion = fields.Text(string='Descripción')
    sequence = fields.Integer(default=1)
    active = fields.Boolean(default=True)
    inicial = fields.Boolean(string='Estado inicial')
    pendiente_correo_acceso = fields.Boolean(string='Pendiente Correo Acceso')
    unattended = fields.Boolean(string='No Procede')
    closed = fields.Boolean(string='Estado final')
    mail_template_id = fields.Many2one('mail.template', string='Email Template',
                                       domain=[('model', '=', 'sicpro.app.soporte')], )
    fold = fields.Boolean(string='Solapado en Kanban')
    company_id = fields.Many2one('res.company', string="Proceso",
                                 default=lambda self: self.env.company)
