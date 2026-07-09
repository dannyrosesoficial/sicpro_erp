# -*- coding: utf-8 -*-

from odoo import fields, models


class RepositorioInstitucionalTipo(models.Model):
    _name = 'sicpro.app.repo.tipo'
    _description = 'Tipos de repositorios'
    _order = 'sequence, name'

    name = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción del estado')
    sequence = fields.Integer('Sequence', default=1)
