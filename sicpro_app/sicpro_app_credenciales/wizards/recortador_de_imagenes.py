# -*- coding: utf-8 -*-


from odoo import api, fields, models, exceptions
from odoo.exceptions import MissingError, UserError


class CredencialesImageCropper(models.TransientModel):
    _name = 'sicpro.app.credenciales.modal'
    _description = 'Credenciales - Modal para recortar Imagen'

    # Cargar por defecto la imagen a recortar,
    # del record activo de credenciales
    def _imagen_del_record_activo(self):
        active_id_credencial = self.env.context.get('active_ids')
        record = self.env['sicpro.app.credenciales'].browse(active_id_credencial)

        img_crop = None
        if active_id_credencial is not None:
            img_crop = record.credencial_image_1920
        return img_crop
    imagen_a_recortar = fields.Image('Imagen a Recortar',
                                     default=_imagen_del_record_activo,
                                     max_width=512, max_height=512)

    # Cerrar la ventana al presionar salvar.
    # La imagen se asignará a credenciales con javascript.
    # solo se cerrará si no existe la barra de recortar
    def action_salvar(self):
        return {'type': 'ir.actions.act_window_close'}






