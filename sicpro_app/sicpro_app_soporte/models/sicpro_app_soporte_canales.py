# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint
from odoo import models, fields, api


class SoporteCanales(models.Model):
    _name = 'sicpro.app.soporte.canales'
    _description = 'Canales de Solicitud'
    _order = "sequence, id"

    @api.model
    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    company_id = fields.Many2one('res.company', string="Proceso",
                                 default=lambda self: self.env.company)
    color = fields.Integer(string='Color',
                           default=_default_color)
    code = fields.Char(string='Código', required=False)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
