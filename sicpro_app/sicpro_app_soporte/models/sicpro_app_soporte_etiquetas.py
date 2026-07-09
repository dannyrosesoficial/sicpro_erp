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


class SoporteEtiquetas(models.Model):
    _name = 'sicpro.app.soporte.etiquetas'
    _description = 'Etiquetas del Soporte'
    _order = "sequence, id"

    active = fields.Boolean(string='Activo', default=True, index=True)
    name = fields.Char(string='Nombre', required=True)
    company_id = fields.Many2one('res.company', string="Company",
                                 default=lambda self: self.env.company)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    solicitudes_acceso = fields.Boolean(string='Etiquetas/Acceso',
                                        default=False, required=False)
