# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO
from odoo import api, Command, fields, models, modules
from datetime import date


def _default_color(self):
    return randint(1, 11)


class AppCMIPerspectivasAnios(models.Model):
    _name = 'sicpro.app.cmi.perspectivas.anios'
    _order = "id asc"
    _description = 'Años de las Perspectivas del CMI'

    def _default_image(self):
        import os
        import base64
        from odoo.modules import get_module_path

        # Obtenemos la ruta base del módulo
        module_path = get_module_path('sicpro_app_cmi')

        if module_path:
            # Construimos la ruta al archivo manualmente
            image_path = os.path.join(module_path, 'static', 'src', 'img', 'etecsaCi_300_8.png')

            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    return base64.b64encode(f.read())

        return False

    name = fields.Char(string='Nombre', required=True, default='DVPE', readonly=True)  # readonly='1' cambiado a True
    user_id = fields.Many2one('res.users', string='Usuario', index=True, default=lambda self: self.env.uid)
    color = fields.Integer(string='Color', default=_default_color)
    active = fields.Boolean(string="Activo", default=True, index=True)
    anio = fields.Char(string="Año", required=True, default=lambda self: str(date.today().year))
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    image_128 = fields.Image("Image", max_width=128, max_height=128, default=_default_image)

    @api.constrains('anio', 'company_id')
    def _check_anio_unicity(self):
        for record in self:
            # Buscamos si existe otro registro con el mismo año y compañía
            domain = [('anio', '=', record.anio), ('company_id', '=', record.company_id.id), ('id', '!=', record.id),

                      ]
            if self.search_count(domain) > 0:
                raise ValidationError("El año %s ya ha sido registrado para el proceso %s. "
                                        "Por favor, verifique los registros existentes.\n\n" % (
                                          record.anio, record.company_id.name) + MSG_SOPORTE_SICPRO)
