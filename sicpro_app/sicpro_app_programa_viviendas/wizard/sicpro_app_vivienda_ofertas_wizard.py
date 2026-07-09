# -*- coding: utf-8 -*-

from random import randint

from odoo import models, fields


def _default_color():
    return randint(1, 11)


class ViviendaOfertas(models.Model):
    _name = 'sicpro.app.vivienda.ofertas'
    _description = 'Ofertas para el programa de la vivienda'

    name = fields.Char('Oferta', required=True)
    proveedor_id = fields.Many2one('sicpro.app.vivienda.proveedor', 'Proveedor', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True, default=lambda self: self.env.uid)
    etapa_id = fields.Many2one('sicpro.app.vivienda.etapas', string='Etapa', required=True)
    fecha = fields.Date(string="Fecha", required=True, default=lambda self: fields.Datetime.now())
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True)
    _sql_constraints = [('name_uniq', 'unique (name)', "¡El nombre de la oferta ya existe!"), ]

    def archivar(self):
        self.active = False

    def desarchivar(self):
        self.active = True
