# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class TrabajadoresEducacionTipos(models.Model):
    _name = 'sicpro.app.trabajadores.educacion.tipos'
    _description = "Tipos de educación del trabajador"
    _order = "sequence"
    _inherit = ['mail.thread']

    name = fields.Char(string='Nombre', required=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Moneda', readonly=True,
                                       related='company_id.currency_id')
    pago = fields.Monetary(string='Pago', tracking=True,
                           currency_field='company_currency', required=True)
    ch = fields.Boolean(string='Certificación', required=False,
                        help='Utilizado en la certificación y homologación de los trabajadores')
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
