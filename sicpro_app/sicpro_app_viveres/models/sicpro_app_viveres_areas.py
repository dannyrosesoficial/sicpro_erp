# -*- coding: utf-8 -*-

from odoo import models, fields


class ViveresAreas(models.Model):
    _name = 'sicpro.app.viveres.areas'
    _description = 'Áreas del módulo de víveres'

    name = fields.Many2one('sicpro.app.trabajadores.areas', string='Área', )
    direccion = fields.Many2one('res.company', string='Dirección', related='name.company_id', store=True, )
    active = fields.Boolean('Activo', default=True)
