# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class RepositorioInstitucionalTipo(models.Model):
    _name = 'sicpro.app.repo.tipo'
    _description = 'Tipos de repositorios'
    _order = 'sequence, name'

    name = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción del estado')
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
