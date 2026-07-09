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
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class AppClientesEtiquetas(models.Model):
    _name = 'sicpro.app.clientes.etiquetas'
    _order = "id asc"
    _description = 'Etiquetas para la Aplicación de Clientes'

    name = fields.Char(string='Etiqueta', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())

    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            domain = [('id', '!=', record.id), ('name', '=ilike', record.name)]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    "¡El nombre de la etiqueta '%s' ya existe!" % record.name)