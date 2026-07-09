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


class RepositorioInstitucionalEtiquetas(models.Model):
    _name = 'sicpro.app.repo.etiquetas'
    _description = 'Etiqueta o Palabra Clave'
    _order = "sequence"

    name = fields.Char(string='Etiqueta', required=True, index=True)
    repositorios_ids = fields.Many2many('sicpro.app.repo', string='Repositorios Asociados')
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
