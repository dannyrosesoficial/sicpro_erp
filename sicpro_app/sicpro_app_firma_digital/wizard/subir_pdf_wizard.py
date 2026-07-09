# -*- coding: utf-8 -*-
import base64

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class FirmaDigitalSubirPDFWizard(models.TransientModel):
    _name = "sicpro.app.firma.subir.pdf.wizard"
    _description = "Subir nuevo documento PDF"

    pdf_original = fields.Many2many('ir.attachment', string="Subir PDF")
    tipo_peticion = fields.Selection(string='Tipo de Petición', required=True, default='simple',
                                     selection=[('simple', 'Único Usuario'), ('multiple', 'Multiples Usuarios'), ], )
    peticiones_usuarios_ids = fields.Many2many('res.users', 'firma_digital_res_users_wizard_rel',
                                               string='Peticiones de Usuarios')
    usuario_responsable_firma = fields.Boolean(string='Usuario_responsable_firma', required=False, default=True)

    # creo nuevo registro
    def subir_pdf(self):
        contador = 0
        for item in self.pdf_original:
            contador += 1
        # controlar que solo se suba un documento al sistema
        if contador > 1:
            raise ValidationError(_("¡Solo debe existir un documento adjunto, si tiene más de uno elimínalo y vuélvalo"
                                    " a intentar!. Si cree que es un error contacte al administrador"))
        else:
            data = base64.b64decode(self.pdf_original.datas)
            nombre = self.pdf_original.name
            if data.startswith(b'%PDF-'):
                ids = self.env['sicpro.app.firma.documentos'].create(
                    {'name': nombre,
                     'pdf_original': self.pdf_original,
                     'tipo_peticion': self.tipo_peticion,
                     'peticiones_usuarios_ids': self.peticiones_usuarios_ids,
                     'usuario_responsable_firma': self.usuario_responsable_firma,
                     })
                # ejecuto la preparación del documento
                ids.preparar_documento()
                # abre el formulario con el registro nuevo
                self.ensure_one()
                action = {
                    'name': _("Firmar Documentos"),
                    'res_model': 'sicpro.app.firma.documentos',
                    'type': 'ir.actions.act_window',
                    'res_id': ids.id,
                    'view_mode': 'form',
                }
                return action
            else:
                raise ValidationError(_("¡Solo se pueden firmar documentos en formato PDF.! "
                                        "Si cree que es un error contacte al administrador"))





