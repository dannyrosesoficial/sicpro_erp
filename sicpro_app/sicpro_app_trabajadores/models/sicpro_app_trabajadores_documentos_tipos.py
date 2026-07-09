# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class TrabajadoresDocumentosTipos(models.Model):
    _name = 'sicpro.app.trabajadores.documentos.tipos'
    _description = 'Tipos de documentos del trabajador'

    name = fields.Char(string="Nombre", required=True)
