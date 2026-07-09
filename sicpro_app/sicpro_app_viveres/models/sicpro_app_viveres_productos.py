# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from random import randint
from odoo import models, fields, api
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO

def _default_color():
    return randint(1, 11)


class ViveresProductos(models.Model):
    _name = 'sicpro.app.viveres.productos'
    _description = "Productos del módulo de víveres"

    name = fields.Char(string='Producto', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    # Todos los campos de imagen están codificados en base64 y son compatibles con PIL
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920", max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512, max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256, max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128, max_height=128, store=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())

    @api.constrains('name')
    def _check_name_control_unique(self):
        for record in self:
            domain = [('name', '=', record.name), ('id', '!=', record.id)]

            if self.search_count(domain) > 0:
                raise ValidationError("¡El nombre del producto '%s' ya existe en el "
                      "sistema!" % record.name + MSG_SOPORTE_SICPRO)
