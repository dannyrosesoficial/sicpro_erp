# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class MenuMarcadores(models.Model):
    _name = 'sicpro.menu.marcadores'
    _description = 'Marcadores'
    _order = 'sequence, name'

    name = fields.Char(string="Nombre", required=True)
    url = fields.Char(string='URL', required=True)
    target = fields.Selection(
        [('_self', 'Pestaña actual'), ('_blank', 'Nueva pestaña')],
        string="Pestaña", default='_self', required=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user,
                              required=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
