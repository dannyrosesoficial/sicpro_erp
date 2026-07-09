# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, fields, models


class CredencialesImageCropper(models.TransientModel):
    _name = 'sicpro.app.credenciales.modal'
    _description = 'Credenciales - Editar Imagen'

    imagen_a_recortar = fields.Image('Imagen a Recortar', max_width=512, max_height=512)

    @api.model
    def default_get(self, fields_list):
        # Este método es el estándar de Odoo para cargar valores iniciales.
        # Es más fiable que una función de default para leer el context.
        res = super(CredencialesImageCropper, self).default_get(fields_list)
        # Obtenemos el ID del registro activo (atendiendo a tu lógica de sicpro)
        active_id = self.env.context.get('active_id') or self.env.context.get('active_ids', [False])[0]

        if active_id:
            # Buscamos el registro de la credencial
            record = self.env['sicpro.app.credenciales'].browse(active_id)
            if record.exists():
                # Asignamos la imagen actual del registro al campo del wizard
                res['imagen_a_recortar'] = record.credencial_image_1920

        return res

    def action_salvar(self):
        """
        Cerrar la ventana al presionar salvar.
        La imagen se asignará de vuelta mediante el bus de eventos en JS.
        """
        return {'type': 'ir.actions.act_window_close'}