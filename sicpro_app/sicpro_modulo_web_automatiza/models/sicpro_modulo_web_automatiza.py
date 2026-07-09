# -*- coding: utf-8 -*-

from odoo import fields, models


class SicproWebAutomatiza(models.Model):
    _name = 'sicpro.modulo.web.automatiza'
    _description = "Nomencladores de asuntos de los correos entrantes"

    name = fields.Char(string='Titulo', required=True,)
    icono = fields.Many2one(comodel_name='sicpro.modulo.dashboard.iconos', string='Nombre Icono',
                                   required=True)
    clase = fields.Char(string='Ícono', related='icono.clase')
    descripcion = fields.Html(string='Descripción', required=True)
    active = fields.Boolean(string="Activo", default=True)

