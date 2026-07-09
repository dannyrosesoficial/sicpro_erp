# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.http import request


class SicproWebManuales(models.Model):
    _name = 'sicpro.modulo.web.manuales'
    _description = 'Manuales de usuarios'
    _order = "sequence, id"

    name = fields.Char('Nombre', required=True)
    descripcion = fields.Char(string='Descripción', required=True)
    clase = fields.Many2one(comodel_name='sicpro.modulo.dashboard.iconos', string='Nombre Icono', required=True)
    icono = fields.Char(string='Ícono', related='clase.clase')
    sequence = fields.Integer('Secuencia', default=1, )
    active = fields.Boolean(string='Archivado', default=True)
    manual = fields.Binary(string="Manual", required=True)
    color = fields.Char(required=True, string='Color')

    # extrae datos del los manuales
    def buscar_datos_manuales(self):
        manuales = self.env['sicpro.modulo.web.manuales'].sudo().search([('active', '=', True)])
        manuales_ids = []
        param_obj = request.env['ir.config_parameter'].sudo()
        base_url = param_obj.get_param('web.base.url')

        for item in manuales:
            data = {'nombre': item.name,
                    'descripcion': item.descripcion,
                    'icono': item.icono,
                    'color': item.color,
                    'manual': base_url + '/web/image?' + 'model=sicpro.modulo.web.manuales&id=' + str(
                        item.id) + '&field=manual',
                    }

            manuales_ids.append(data)
        return manuales_ids
