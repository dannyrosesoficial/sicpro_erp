# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'
    _order = 'id'

    jefe_proceso = fields.Many2one(comodel_name='sicpro.app.trabajadores',
                                   string='Jefe del Proceso', required=False)
