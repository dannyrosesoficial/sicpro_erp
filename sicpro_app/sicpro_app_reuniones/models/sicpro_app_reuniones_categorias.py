# -*- coding: utf-8 -*-

from random import randint

from odoo import api, fields, models


class ReunionesEtiquetasCategorias(models.Model):
    _name = "sicpro.app.reuniones.categorias"
    _description = "Categorías de las etiquetas"
    _order = "sequence"

    name = fields.Char("Nombre", required=True, translate=True)
    sequence = fields.Integer('Sequence', default=0)
    etiquetas_ids = fields.One2many('sicpro.app.reuniones.etiquetas',
                                    'categoria_id', string="Etiquetas")
