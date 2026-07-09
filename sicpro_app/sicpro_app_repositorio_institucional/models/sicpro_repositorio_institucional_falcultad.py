# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class RepositorioInstitucionalFacultad(models.Model):
    _name = 'sicpro.app.repo.facultad'
    _description = 'Facultad o Universidad'

    name = fields.Char(string='Nombre de la Institución', required=True)
    parent_id = fields.Many2one('sicpro.app.repo.facultad', string='Unidad Superior')
    repositorio_ids = fields.One2many('sicpro.app.repo', 'facultad_id',
                                      string='Publicaciones de la Unidad')
    descripcion = fields.Text(string='Condiciones de Uso')
    sequence = fields.Integer('Sequence', default=0)
