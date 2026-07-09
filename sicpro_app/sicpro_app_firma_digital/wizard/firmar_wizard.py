# -*- coding: utf-8 -*-
import base64
import datetime
import io

from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from endesive import pdf

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import config


class FirmaDigitalWizard(models.TransientModel):
    _name = 'sicpro.app.firma.wizard'
    _description = "Firmar Wizard"

    @api.model
    def _sign_doc(self):
        doc = self._context.get('active_model') == 'sicpro.app.firma.documentos' and self._context.get(
            'active_ids') or []
        for item in self.env['sicpro.app.firma.documentos'].browse(doc):
            return item

    doc_id = fields.Many2one(comodel_name='sicpro.app.firma.documentos', string='Documento', default=_sign_doc,
                             required=True)
    doc_imagenes_ids = fields.One2many(comodel_name='sicpro.app.firma.documentos.imagenes', inverse_name='name',
                                       string='Imágenes', related='doc_id.doc_imagenes_ids')
    doc_firma = fields.Binary(string="Firma Digital", required=True)
    password = fields.Char(string='Contraseña', required=True)

    def firmar_documento(self):
        doc_coord_width = 0
        doc_coord_height = 0
        coord_x_cropper = 0
        coord_y_cropper = 0
        coord_w_cropper = 0
        coord_h_cropper = 0
        doc_num_page = 0

        # busco las coordenadas de la página seleccionada
        for item in self.doc_imagenes_ids:
            if item.doc_firmar:
                doc_coord_width = item.doc_ancho
                doc_coord_height = item.doc_alto
                coord_x_cropper = item.doc_crop_izq
                coord_y_cropper = item.doc_crop_der
                coord_w_cropper = item.doc_crop_ancho
                coord_h_cropper = item.doc_crop_alto
                doc_num_page = item.doc_num_page

        coord_x = coord_x_cropper
        coord_y = doc_coord_height - coord_y_cropper - coord_h_cropper
        coord_w = coord_x + coord_w_cropper
        coord_h = coord_y + coord_h_cropper

        try:
            password = self.password
            usuario = self.env['res.users'].search([('id', '=', self.env.uid)])
            # Creo la ruta de la firma escrita del data/filestore
            store_fname = str(usuario.firma_imagen.store_fname)
            direct = str(config['data_dir']) + str('/filestore/') + str(self.env.cr.dbname) + str('/')
            img_firma = direct + store_fname
            # numero de la pagina a firmar
            pagina_firma = doc_num_page
            # fecha de la firma
            fecha = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
            fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")
            # coordenadas de la firma
            coordenadas = (coord_x, coord_y, coord_w, coord_h)
            # cargo el certificado digital y salvo en buffer
            certificado_digital = io.BytesIO(base64.b64decode(self.doc_firma)).read()
            p12 = pkcs12.load_key_and_certificates(certificado_digital, password.encode(), backends.default_backend())
            # obtener el nombre del usuario de la certificación digital
            contacto = None
            p12_contacto = str(p12[1]).split(",")
            for contact in p12_contacto:
                if contact[0:2] == 'CN':
                    contacto = contact[3:len(contact)]
            # creo el diccionario con el diseño de la firma
            dct = {"aligned": 0, "sigflags": 3, "sigflagsft": 132, "sigpage": pagina_firma, "auto_sigfield": True,
                   "signaturebox": coordenadas, "signform": False, "sigfield": "Signature", "sigandcertify": True,
                   "signature_manual": [  # RGB
                       # ['fill_colour', 0.95, 0.95, 0.95],
                       # *[bounding box]
                       # ['rect_fill', 10, 10, 270, 18],
                       # RGB
                       # ['stroke_colour', 0, 0, 0],  # inset
                       # ['border', 2],  # key  *[bounding box] distort centred
                       ['image', 'sig0', 0, 25, 80, 120, False, False],  # font     fs
                       ['font', 'default', 12],  # R  G  B
                       ['fill_colour', 0, 0, 0],  # text
                       ['text_box', 'Firmado digitalmente por\n' + str(contacto) + '\n{}'.format(fecha) + '\nSICPRO ERP',
                        #  font  * [bounding box],fs,   wrap, align, baseline
                        'default', 80, 50, 270, 18, 8, True, 'left', 'top'], ],
                   # key: nombre utilizado en directivas de imagen
                   # value: PIL Objeto de imagen o ruta al archivo de imagen
                   "manual_images": {'sig0': img_firma},  # key: nombre utilizado en directivas de fuentes
                   # value: ruta al archivo de fuente TTF
                   "manual_fonts": {}, "contact": contacto, "location": "Cuba", "signingdate": fecha,
                   "reason": "Firmado con SICPRO ERP. DVPE - ETECSA", "password": password, }

            # salvando pdf original en buffer
            pdf_original = io.BytesIO(base64.b64decode(self.doc_id.pdf_original.datas)).read()
            # aplicando firma
            datas = pdf.cms.sign(pdf_original, dct, p12[0], p12[1], p12[2], "sha256")
            # género el documento pdf firmado y lo guardo en el campo seleccionado
            with io.BytesIO() as f:
                f.write(pdf_original)
                f.write(datas)
                # guardo el documento en el filestore y devuelvo el, id
                attachment_id = self.env['ir.attachment'].create(
                    {'name': self.doc_id.name,
                     'res_model': 'sicpro.app.firma.documentos',
                     'datas': base64.b64encode(f.getvalue())
                     })
                self.doc_id.pdf_firmado = attachment_id.id
                # cambio el estado del documento ha firmado
                self.doc_id.estados = 'firmado'

            # recargo la pagina
            return {'type': 'ir.actions.client', 'tag': 'reload', }

        except ValueError as e:
            raise ValidationError(_("Ha habido un problema con el certificado, algunos problemas habituales pueden ser:\n"
                                    "- La contraseña proporcionada o el certificado no son válidos.\n"
                                    "- El contenido del certificado no es válido.\n"
                                    "- Si cree que es un error contacte al administrador.\n"))
