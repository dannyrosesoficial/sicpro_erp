# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class SicproWebGaleriaEtiquetas(models.Model):
    _name = 'sicpro.modulo.web.galeria.etiquetas'
    _description = 'Etiquetas de la Galería'
    _order = "sequence, id"

    name = fields.Char('Etiqueta', required=True)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    sequence = fields.Integer('Secuencia', default=1, )
    active = fields.Boolean(string='Archivado', default=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la etiqueta existe!"), ]
