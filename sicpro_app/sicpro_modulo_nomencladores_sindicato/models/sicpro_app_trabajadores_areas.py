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


class Departamentos(models.Model):
    _inherit = "sicpro.app.trabajadores.areas"

    seccion_sindical_id = fields.Many2one("sicpro.nomenclador.sindicato",
                                          string="Sección Sindical",
                                          tracking=True)
