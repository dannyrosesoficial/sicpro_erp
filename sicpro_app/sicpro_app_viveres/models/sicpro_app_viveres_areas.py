# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class ViveresAreas(models.Model):
    _name = 'sicpro.app.viveres.areas'
    _description = 'Áreas del módulo de víveres'

    name = fields.Many2one('sicpro.app.trabajadores.areas', string='Área', )
    direccion = fields.Many2one('res.company', string='Dirección',
                                related='name.company_id', store=True, )
    active = fields.Boolean(string='Activo', default=True, index=True)
