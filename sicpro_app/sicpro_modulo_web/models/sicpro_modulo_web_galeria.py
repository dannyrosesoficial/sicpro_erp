# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api


class SicproWebGaleria(models.Model):
    _name = 'sicpro.modulo.web.galeria'
    _description = 'Imágenes de la Galería'
    _order = "sequence, id"

    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    image_1920 = fields.Image("Imagen", max_width=1920, max_height=1920)
    tipo = fields.Selection(string='Tipo', default='normal', required=True,
                            selection=[('normal', 'Normal'), ('tall', 'Alto'),
                                       ('wide', 'Ancho'),
                                       ('wide_tall', 'Alto y Ancho')])

    @api.model
    def buscar_datos_img(self):
        img_records = self.sudo().search([('active', '=', True)])
        img_list = []

        for item in img_records:
            img_list.append(
                {'id': item.id, 'nombre': item.name, 'tipo': item.tipo,
                    'imagen': f'/web/image/sicpro.modulo.web.galeria/{item.id}/image_1920'})
        return img_list
