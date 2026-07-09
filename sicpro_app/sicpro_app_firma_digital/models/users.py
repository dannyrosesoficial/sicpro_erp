# -*- coding: utf-8 -*-
import base64
import io

from PIL import Image

from odoo import models, fields, api


class Users(models.Model):
    _inherit = "res.users"

    firma_digital = fields.Binary(string="Firma Digital")
    firma_imagen = fields.Many2one('ir.attachment', string="Firma")

    @api.onchange('firma_digital')
    def _firma_digital_imagen(self):
        # elimino el registro de firmas anterior
        self.env['ir.attachment'].search([('id', '=', self.firma_imagen.id)]).unlink()

        # creo la imagen de la firma con Pil
        img_binary = self.firma_digital.decode('utf-8')
        img = Image.open(io.BytesIO(base64.decodebytes(bytes(img_binary, "utf-8"))))
        buffered = io.BytesIO()
        img.save(buffered, format="png")

        # creo el registro de la imagen en el filestore
        attachment = self.env['ir.attachment'].create(
            {'name': 'Firma_' + str(self.name) + '.png', 'datas': base64.b64encode(buffered.getvalue()),
             'res_model': 'res.users', 'res_id': self.id, 'type': 'binary',
             'mimetype': 'image/png', })
        # guardo él, id del vínculo creado con ir.attachment
        self.firma_imagen = attachment

