# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models


class PartesHoras(models.Model):
    _name = 'sicpro.app.partes.horas'
    _description = 'Partes de horas'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    # devuelve el usuario actual de la aplicación
    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    # devuelve el id del trabajador del especialista ejecutor
    @api.model
    def _default_trabajador(self):
        especialista = self.env[
            'sicpro.app.trabajadores.general'].search(
            [('user_id', '=', self.env.user.id), ], limit=1).id
        return especialista

    name = fields.Char('Descripción', required=True)
    fecha = fields.Date('Fecha', required=True, index=True,
                        default=fields.Date.context_today)
    user_id = fields.Many2one('res.users', string='Usuario',
                              default=_default_user)
    especialista_ejecutor_id = fields.Many2one(
        'sicpro.app.preparacion.tecnica.ejecutor', 'Especialista', )
    preparaciones = fields.Many2one(
        'sicpro.app.preparacion.tecnica.preparaciones', 'Preparaciones',
        index=True, domain="[('company_id', '=', company_id)]")
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True, readonly=True,
                                 default=lambda self: self.env.company)
    trabajador = fields.Many2one(
        comodel_name="sicpro.app.trabajadores.general",
        string="Trabajador", index=True, required=False, readonly=True,
        tracking=True, domain="[('company_id', '=', company_id)]",
                              default=_default_trabajador)
    departamento = fields.Many2one(
        'sicpro.app.trabajadores.departmentos', string="Departamento",
        compute='_compute_department_id', store=True, compute_sudo=True)
    currency_id = fields.Many2one(related="company_id.currency_id",
                                  string="Currency", readonly=True, store=True,
                                  compute_sudo=True)
    importe = fields.Monetary('Importe', required=True, default=0.0)
    duracion = fields.Float('Duración (Horas)', default=0.0)

    start_date = fields.Datetime(string='Fecha inicial')
    end_date = fields.Datetime(string='Fecha fin')

    # busca el especialista mediante la preparación
    @api.onchange('preparaciones')
    def _onchange_preparaciones(self):
        if not self.especialista_ejecutor_id:
            self.especialista_ejecutor_id = self.preparaciones.especialista_ejecutor_id

    # actualiza el usuario en dependencia del trabajador
    @api.onchange('trabajador')
    def _onchange_trabajador(self):
        if self.trabajador:
            self.user_id = self.trabajador.user_id
        else:
            self.user_id = self._default_user()

    # actualiza el departamento en dependencia del trabajador
    @api.depends('trabajador')
    def _compute_department_id(self):
        for line in self:
            line.departamento = line.trabajador.department_id

    @api.model
    def create(self, values):
        # Agrego el trabajador automáticamente
        if not values.get('trabajador') and values.get('preparaciones'):
            if values.get('user_id'):
                ts_user_id = values['user_id']
            else:
                ts_user_id = self._default_user()
            values['trabajador'] = self.env[
                'sicpro.app.trabajadores.general'].search(
                [('user_id', '=', ts_user_id)], limit=1).id
        result = super(PartesHoras, self).create(values)
        return result
