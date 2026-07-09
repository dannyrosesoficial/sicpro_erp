# -*- coding: utf-8 -*-


from odoo import models, fields


class HrEmployeeAttachment(models.Model):
    _inherit = 'ir.attachment'

    doc_attach_rel = fields.Many2many('sicpro.app.trabajadores.documentos', 'doc_attachment_id', 'attach_id3', 'doc_id',
                                      string="Adjunto", invisible=1)
    attach_rel = fields.Many2many('sicpro.app.trabajadores.documentos.plantillas', 'attach_id', 'attachment_id3',
                                  'document_id', string="Adjuntos", invisible=1)
