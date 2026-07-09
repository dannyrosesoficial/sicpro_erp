# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class TrabajadoresCursosHabilidades(models.Model):
    _name = 'sicpro.app.trabajadores.cursos.habilidades'
    _description = 'Habilidades de los trabajadores'

    name = fields.Char(string='Nombre', required=True)
    skill_type_id = fields.Many2one('sicpro.app.trabajadores.cursos.tipos',
                                    ondelete='cascade')
