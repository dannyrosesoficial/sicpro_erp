# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request


class SicproWebAbout(models.Model):
    _name = 'sicpro.modulo.web.about'
    _description = 'Link de Acceso al video de Introducción'

    name = fields.Char(string='Video', required=True, default='Video de Introducción')
    active = fields.Boolean(string='Archivado', default=True)
    video = fields.Binary(string="Url Video")
    url_computado = fields.Char(string='Url_computado', compute="compute_buscar_datos_video")

    @api.constrains('active')
    def _check_id_unico(self):
        uniq = self.env['sicpro.modulo.web.about'].search(['&', ("active", "=", True), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡Ya se encuentra una url configurada!. "
                                    "Si cree que es un error contacte al administrador"))

    # extrae video introductorio
    def compute_buscar_datos_video(self):
        param_obj = request.env['ir.config_parameter'].sudo()
        base_url = param_obj.get_param('web.base.url')

        for item in self:
            item.url_computado = base_url + '/web/image?' + 'model=sicpro.modulo.web.about&id=' + str(
                        item.id) + '&field=video'


