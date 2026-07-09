# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"
    
    def session_info(self):
        result = super().session_info()

        # Obtenemos el parámetro global de la configuración
        bg_image = self.env['ir.config_parameter'].sudo().get_param(
            'sicpro.theme_background_image')

        # Solo inyectamos el valor global para que el frontend lo use siempre
        result.update({'theme_background_image': bg_image,
            'has_background_image': bool(bg_image), })

        return result
