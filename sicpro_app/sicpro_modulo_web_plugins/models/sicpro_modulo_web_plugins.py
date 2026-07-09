# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.http import request


class SicproWebPlugins(models.Model):
    _name = 'sicpro.modulo.web.plugins'
    _description = "Listado de aplicaciones y plugins para descargar y utilizar con SICPRO ERP"
    _order = "sequence, id"

    name = fields.Char(string='Nombre', required=True,)
    sequence = fields.Integer('Secuencia', default=1, )
    tipo = fields.Selection(
        string='Tipo',
        selection=[('plugins', 'Plugins'), ('app', 'Aplicación'), ], required=True, )
    descripcion = fields.Html(string='Descripción', required=True)
    active = fields.Boolean(string="Activo", default=True)
    plataforma = fields.Selection(string='Plataforma',
                                  selection=[('android', 'Android'), ('ios', 'IOS'),
                                             ('linux', 'Linux'), ('windows', 'Windows'), ], required=True,)
    archivo = fields.Binary(string="Archivo")
    popular = fields.Boolean(string='Popular', required=False, default=False)

    # extrae datos de los plugins
    def buscar_datos_plugins(self):
        plugins = self.env['sicpro.modulo.web.plugins'].search([('active', '=', True)])
        plugins_ids = []
        param_obj = request.env['ir.config_parameter'].sudo()
        base_url = param_obj.get_param('web.base.url')

        # compruebo que sea un plugin favorito
        for item in plugins:
            if item.popular:
                popular = 'popular'
            else:
                popular = ''

            data = {
                'nombre': item.name,
                'tipo': dict(item._fields['tipo'].selection).get(item.tipo),
                'popular': popular,
                'descripcion': item.descripcion,
                'plataforma': dict(item._fields['plataforma'].selection).get(item.plataforma),
                'archivo': base_url + '/web/content?' + 'model=sicpro.modulo.web.plugins&download=true&field=archivo&filename=' + str(item.name) + '.zip&id=' + str(item.id),
            }
            plugins_ids.append(data)
        return plugins_ids


