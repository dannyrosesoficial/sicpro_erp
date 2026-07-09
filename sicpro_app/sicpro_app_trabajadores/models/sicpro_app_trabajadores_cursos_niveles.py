# -*- coding: utf-8 -*-

from odoo import api, fields, models


class TrabajadoresCursosNiveles(models.Model):
    _name = 'sicpro.app.trabajadores.cursos.niveles'
    _description = 'Niveles de los cursos del trabajador'
    _order = "level_progress desc"

    skill_type_id = fields.Many2one('sicpro.app.trabajadores.cursos.tipos',
                                    string='Curso', ondelete='cascade')
    name = fields.Char(string='Nombre', required=True)
    level_progress = fields.Integer(string="Progreso")
