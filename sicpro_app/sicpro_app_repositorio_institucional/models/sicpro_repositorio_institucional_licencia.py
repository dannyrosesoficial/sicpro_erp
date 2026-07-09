# -*- coding: utf-8 -*-

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
    sequence = fields.Integer('Sequence', default=0)
