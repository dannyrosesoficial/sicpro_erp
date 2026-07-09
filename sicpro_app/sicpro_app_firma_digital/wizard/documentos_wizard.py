# -*- coding: utf-8 -*-

from odoo import fields, models, api


class FirmaDigitalDocumentosWizard(models.TransientModel):
    _name = 'sicpro.app.firma.documentos.wizard'
    _description = "Documento Wizard"

    @api.model
    def _sign_doc(self):
        doc = self._context.get('active_model') == 'sicpro.app.firma.documentos' and self._context.get(
            'active_ids') or []
        for item in self.env['sicpro.app.firma.documentos'].browse(doc):
            return item

    doc_id = fields.Many2one(comodel_name='sicpro.app.firma.documentos', string='Documento', default=_sign_doc,
                             required=True)
    doc_imagenes_ids = fields.One2many(comodel_name='sicpro.app.firma.documentos.imagenes',
                                       related='doc_id.doc_imagenes_ids')
