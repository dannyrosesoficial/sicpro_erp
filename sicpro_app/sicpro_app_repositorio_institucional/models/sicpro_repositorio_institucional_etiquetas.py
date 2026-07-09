# -*- coding: utf-8 -*-

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
    sequence = fields.Integer('Sequence', default=0)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
