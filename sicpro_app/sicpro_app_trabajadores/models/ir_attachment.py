# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models, fields


class HrEmployeeAttachment(models.Model):
    _inherit = 'ir.attachment'

    doc_attach_rel = fields.Many2many('sicpro.app.trabajadores.documentos',
                                      'doc_attachment_id', 'attach_id3',
                                      'doc_id', string="Adjunto")
    attach_rel = fields.Many2many(
        'sicpro.app.trabajadores.documentos.plantillas', 'attach_id',
        'attachment_id3', 'document_id', string="Adjuntos")
