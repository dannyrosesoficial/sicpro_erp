# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.http import request


class SicproWebGaleria(models.Model):
    _name = 'sicpro.modulo.web.galeria'
    _description = 'Imágenes de la Galería'

    name = fields.Char('Nombre', required=True)
    etiquetas = fields.Many2many('sicpro.modulo.web.galeria.etiquetas', 'sicpro_modulo_web_galeria_etiquetas_rel',
                                 string='Etiqueta')
    active = fields.Boolean(string='Archivado', default=True)
    image = fields.Binary(string="Imagen")

    # extrae datos de la galería
    def buscar_datos_img(self):
        img = self.env['sicpro.modulo.web.galeria'].search([('active', '=', True)])
        img_ids = []
        param_obj = request.env['ir.config_parameter'].sudo()
        base_url = param_obj.get_param('web.base.url')

        for item in img:
            etiqueta = ''
            for value in item.etiquetas:
                etiqueta += str(value.name) + ' '

            data = {'nombre': item.name, 'etiquetas': etiqueta,
                    'imagen': base_url + '/web/image?' + 'model=sicpro.modulo.web.galeria&id=' + str(
                        item.id) + '&field=image', }

            img_ids.append(data)
        return img_ids
