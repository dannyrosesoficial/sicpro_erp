# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint

from odoo import models, fields


def _default_color():
    return randint(1, 11)


class TrabajadoresGeneral(models.Model):
    _inherit = 'sicpro.app.trabajadores'

    seccion_sindical_id = fields.Many2one("sicpro.nomenclador.sindicato",
                                          string="Sección Sindical",
                                          related='area_id.seccion_sindical_id',
                                          tracking=True)
