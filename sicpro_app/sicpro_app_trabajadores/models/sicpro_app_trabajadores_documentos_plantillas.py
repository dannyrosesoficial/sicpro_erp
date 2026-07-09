# -*- coding: utf-8 -*-

from odoo import models, fields


class TrabajadoresDocumentosPlantillas(models.Model):
    _name = 'sicpro.app.trabajadores.documentos.plantillas'
    _description = 'Plantillas de documentos del trabajador'

    name = fields.Char(string='Nombre del Documento', required=True, copy=False, )
    notas = fields.Text(string='Notas', copy=False)
    attach_id = fields.Many2many('ir.attachment', 'attach_rel', 'doc_id', 'attach_id3', string="Adjunto", copy=False)
