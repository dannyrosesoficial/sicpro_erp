# -*- coding: utf-8 -*-

from odoo import api, fields, models


class TrabajadoresEducacionTipos(models.Model):
    _name = 'sicpro.app.trabajadores.educacion.tipos'
    _description = "Tipos de educación del trabajador"
    _order = "sequence"
    _inherit = ['mail.thread']

    name = fields.Char(string='Nombre', required=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Currency', readonly=True,
                                       related='company_id.currency_id')
    pago = fields.Monetary('Pago', tracking=True,
                           currency_field='company_currency', required=True)
    ch = fields.Boolean(
        string='Certificación', required=False,
        help='Utilizado en la certificación y homologación del trabajadores')

    sequence = fields.Integer('Sequence', default=10)
