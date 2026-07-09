# -*- coding: utf-8 -*-

from odoo import fields, models
from random import randint

Niveles = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'), ('3', 'Muy Alta'), ]


class SalonClasesTemas(models.Model):
    _name = "sicpro.app.salon.clases.temas"
    _description = "Temas del Salón de clases"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "name, id"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Temática", index=True, required=True,
                       tracking=True, )
    nivel = fields.Selection(Niveles, string='Nivel', index=True,
                             tracking=True, default=Niveles[0][0])
    active = fields.Boolean(default=True, )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    color = fields.Integer(string='Color Index',
                           default=lambda self: self._default_color())
    user_id = fields.Many2one('res.users', string='Organizador',
                              default=lambda self: self.env.uid, index=True,
                              tracking=True)
    tipo = fields.Many2one(comodel_name='sicpro.app.salon.clases.tipo',
                           string='Tipo', required=True)
    favorito = fields.Boolean(string='Favorito', required=False)
    description = fields.Html(string='Descripción')
    clases_count = fields.Integer(compute='_compute_clases_count',
                                  string="Cuenta las Clases")

    def _compute_clases_count(self):
        data = self.env['sicpro.app.salon.clases']
        for clases in self:
            clases.clases_count = data.search_count([
                ('temas_id', '=', clases.id)])