# -*- coding: utf-8 -*-

from random import randint
from odoo import api, fields, models


class ReunionesEtiquetas(models.Model):
    _name = "sicpro.app.reuniones.etiquetas"
    _description = "Etiqueta de las Reuniones"
    _order = "sequence"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char("Nombre", required=True, translate=True)
    sequence = fields.Integer('Sequence', default=0)
    categoria_id = fields.Many2one("sicpro.app.reuniones.categorias",
                                   string="Categoría", required=True,
                                   ondelete='cascade')
    color = fields.Integer(
        string='Color Index', default=lambda self: self._default_color())
    usuarios_ids = fields.Many2many('res.users', string="Usuarios",
                                    readonly=False, store=True, )

    def name_get(self):
        return [(tag.id, "%s: %s" % (tag.categoria_id.name, tag.name))
                for tag in self]
