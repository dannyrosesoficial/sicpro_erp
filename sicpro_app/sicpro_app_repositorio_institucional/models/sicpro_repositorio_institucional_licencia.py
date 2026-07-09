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


class RepositorioInstitucionalLicencia(models.Model):
    _name = 'sicpro.app.repo.licencia'
    _description = 'Licencias de Uso'

    name = fields.Char(string='Nombre de la Licencia', required=True)
    siglas = fields.Char(string='Siglas', required=True)
    url = fields.Char(string='URL de la Licencia')
    description = fields.Text(string='Condiciones de Uso')
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
