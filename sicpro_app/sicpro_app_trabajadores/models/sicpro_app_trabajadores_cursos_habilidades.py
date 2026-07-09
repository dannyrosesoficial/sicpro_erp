# -*- coding: utf-8 -*-

from odoo import fields, models


class TrabajadoresCursosHabilidades(models.Model):
    _name = 'sicpro.app.trabajadores.cursos.habilidades'
    _description = 'Habilidades de los trabajadores'

    name = fields.Char(string='Nombre', required=True)
    skill_type_id = fields.Many2one('sicpro.app.trabajadores.cursos.tipos', ondelete='cascade')
