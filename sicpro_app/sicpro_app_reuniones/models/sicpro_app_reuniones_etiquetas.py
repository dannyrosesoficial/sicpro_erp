# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint
from odoo import fields, models, api


class ReunionesEtiquetas(models.Model):
    _name = "sicpro.app.reuniones.etiquetas"
    _description = "Etiqueta de las Reuniones"
    _order = "sequence"

    @api.model
    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Nombre", required=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    categoria_id = fields.Many2one("sicpro.app.reuniones.categorias",
                                   string="Categoría", required=True,
                                   ondelete='cascade')
    color = fields.Integer(string='Color',
                           default=_default_color)
    usuarios_ids = fields.Many2many('res.users', string="Usuarios",
                                    readonly=False, store=True, )
    despacho = fields.Boolean(string='Despacho', required=False, default=False)

    def name_get(self):
        return [(tag.id, "%s: %s" % (tag.categoria_id.name, tag.name)) for tag
                in self]
