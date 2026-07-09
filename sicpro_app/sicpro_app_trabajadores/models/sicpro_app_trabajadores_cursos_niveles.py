# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class TrabajadoresCursosNiveles(models.Model):
    _name = 'sicpro.app.trabajadores.cursos.niveles'
    _description = 'Niveles de los cursos del trabajador'
    _order = "level_progress desc"

    skill_type_id = fields.Many2one('sicpro.app.trabajadores.cursos.tipos',
                                    string='Curso', ondelete='cascade')
    name = fields.Char(string='Nombre', required=True)
    level_progress = fields.Integer(string="Progreso")
