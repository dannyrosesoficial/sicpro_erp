# -*- coding: utf-8 -*-


from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class FirmaDigitalDocumentosImagenes(models.Model):
    _name = 'sicpro.app.firma.documentos.imagenes'
    _description = 'Imágenes del PDF de la Firma Digital'
    _order = 'id asc'

    name = fields.Many2one(comodel_name='sicpro.app.firma.documentos', string='Documento', required=False)
    doc_imagen = fields.Image('Imagen')
    doc_num_page = fields.Integer(string='Página', required=False)
    doc_ancho = fields.Integer(string='Ancho')
    doc_alto = fields.Integer(string='Alto')
    doc_crop_izq = fields.Float(string='doc. izq', required=False)
    doc_crop_der = fields.Float(string='doc. der', required=False)
    doc_crop_ancho = fields.Float(string='doc. ancho', required=False)
    doc_crop_alto = fields.Float(string='doc. alto', required=False)
    doc_firmar = fields.Boolean(string='Firmar Página', required=False, default=False)

    # Cerrar la ventana del selector de firma al presionar salvar.
    def action_salvar(self):
        return {'type': 'ir.actions.client', 'tag': 'reload', }

    # actualizo las coordenadas de la imagen con los datos enviados del cropper_pdf de javascript
    @api.model
    def actualizar_coordenadas(self, imagen_id, coord):
        img_id = imagen_id.get('imagen_id')
        if len(coord[0]) == 7:
            # actualizo las coordenadas
            self.env['sicpro.app.firma.documentos.imagenes'].search([('id', '=', img_id)]).write(
                {'doc_crop_izq': coord[0][0], 'doc_crop_der': coord[0][1], 'doc_crop_ancho': coord[0][2],
                 'doc_crop_alto': coord[0][3], 'doc_firmar': True, })
            # actualizo el estado del documento
            res_id = self.env['sicpro.app.firma.documentos.imagenes'].search([('id', '=', img_id)])
            res_id.name.estados = 'gestion_firma'
        else:
            raise ValidationError(_("¡Error al seleccionar el área de firma, inténtelo nuevamente!. "
                                    "Si cree que es un error contacte al administrador"))
