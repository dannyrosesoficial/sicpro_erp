# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class TrabajadoresDocumentosPlantillas(models.Model):
    _name = 'sicpro.app.trabajadores.documentos.plantillas'
    _description = 'Plantillas de documentos del trabajador'

    name = fields.Char(string='Nombre del Documento', required=True,
                       copy=False, )
    notas = fields.Text(string='Notas', copy=False)
    attach_id = fields.Many2many('ir.attachment', 'attach_rel', 'doc_id',
                                 'attach_id3', string="Adjunto", copy=False)
