# -*- coding: utf-8 -*-
from odoo.http import Controller, route


class FirmaDigitalOriginID(Controller):

    @route('/sicpro_app_firma_digital/download/doc/origin_id', type='json', auth='user')
    def firma_digital_doc_origin(self, **kw):
        res_id = 19
        value = self.env['sicpro.app.firma.documentos'].search(['id', '=', res_id]).pdf_firmado.id

        print(value)
        url = '/web/binary/download_document?tab_id=%s' % value
        return {'type': 'ir.actions.act_url', 'url': url, 'target': 'new', }

