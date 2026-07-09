# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class TrabajadoresCursosTipos(models.Model):
    _name = 'sicpro.app.trabajadores.cursos.tipos'
    _description = 'Tipos de cursos del trabajador'

    name = fields.Char(string='Nombre', required=True)
    skill_ids = fields.One2many('sicpro.app.trabajadores.cursos.habilidades',
                                'skill_type_id', string="Habilidades")
    skill_level_ids = fields.One2many('sicpro.app.trabajadores.cursos.niveles',
                                      'skill_type_id', string="Niveles")
