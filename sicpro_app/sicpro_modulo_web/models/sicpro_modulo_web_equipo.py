# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.http import request


class SicproWebEquipo(models.Model):
    _name = 'sicpro.modulo.web.equipo'
    _description = 'Equipo de Desarrollo'
    _order = "sequence, id"

    name = fields.Char('Nombre', required=True)
    cargo = fields.Char(string='Cargo', required=True)
    responsabilidad = fields.Html(string='Responsabilidad', required=True)
    cuenta_twitter = fields.Char(string='Twitter', required=False)
    cuenta_facebook = fields.Char(string='Facebook', required=False)
    cuenta_instagram = fields.Char(string='Instagram', required=False)
    cuenta_linkedin = fields.Char(string='Linkedin', required=False)
    cuenta_correo = fields.Char(string='Correo', required=False)
    sequence = fields.Integer('Secuencia', default=1, )
    active = fields.Boolean(string='Archivado', default=True)
    image = fields.Binary(string="Imagen")

    # extrae datos del equipo
    def buscar_datos_equipos(self):
        equipos = self.env['sicpro.modulo.web.equipo'].sudo().search([('active', '=', True)])
        equipos_ids = []
        param_obj = request.env['ir.config_parameter'].sudo()
        base_url = param_obj.get_param('web.base.url')

        for item in equipos:
            data = {'nombre': item.name,
                    'cargo': item.cargo,
                    'responsabilidad': item.responsabilidad,
                    'twitter': item.cuenta_twitter,
                    'facebook': item.cuenta_facebook,
                    'instagram': item.cuenta_instagram,
                    'linkedin': item.cuenta_linkedin,
                    'correo': item.cuenta_correo,
                    'imagen': base_url + '/web/image?' + 'model=sicpro.modulo.web.equipo&id=' + str(
                        item.id) + '&field=image', }

            equipos_ids.append(data)
        return equipos_ids
