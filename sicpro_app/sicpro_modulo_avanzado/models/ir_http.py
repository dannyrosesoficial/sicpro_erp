# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        config_parameter = request.env['ir.config_parameter'].sudo()
        result['app_system_name'] = config_parameter.get_param('app_system_name')
        result['app_menu_perfil_1'] = config_parameter.get_param('app_menu_perfil_1')
        result['app_menu_perfil_1_titulo'] = config_parameter.get_param('app_menu_perfil_1_titulo')
        result['app_menu_perfil_1_url'] = config_parameter.get_param('app_menu_perfil_1_url')
        result['app_menu_perfil_1_sequence'] = config_parameter.get_param('app_menu_perfil_1_sequence')
        result['app_menu_perfil_2'] = config_parameter.get_param('app_menu_perfil_2')
        result['app_menu_perfil_2_titulo'] = config_parameter.get_param('app_menu_perfil_2_titulo')
        result['app_menu_perfil_2_url'] = config_parameter.get_param('app_menu_perfil_2_url')
        result['app_menu_perfil_2_sequence'] = config_parameter.get_param('app_menu_perfil_2_sequence')
        result['app_menu_perfil_3'] = config_parameter.get_param('app_menu_perfil_3')
        result['app_menu_perfil_3_titulo'] = config_parameter.get_param('app_menu_perfil_3_titulo')
        result['app_menu_perfil_3_url'] = config_parameter.get_param('app_menu_perfil_3_url')
        result['app_menu_perfil_3_sequence'] = config_parameter.get_param('app_menu_perfil_3_sequence')
        result['app_menu_perfil_4'] = config_parameter.get_param('app_menu_perfil_4')
        result['app_menu_perfil_4_titulo'] = config_parameter.get_param('app_menu_perfil_4_titulo')
        result['app_menu_perfil_4_url'] = config_parameter.get_param('app_menu_perfil_4_url')
        result['app_menu_perfil_4_sequence'] = config_parameter.get_param('app_menu_perfil_4_sequence')
        result['app_menu_perfil_5'] = config_parameter.get_param('app_menu_perfil_5')
        result['app_menu_perfil_5_titulo'] = config_parameter.get_param('app_menu_perfil_5_titulo')
        result['app_menu_perfil_5_url'] = config_parameter.get_param('app_menu_perfil_5_url')
        result['app_menu_perfil_5_sequence'] = config_parameter.get_param('app_menu_perfil_5_sequence')
        result['app_menu_perfil_6'] = config_parameter.get_param('app_menu_perfil_6')
        result['app_menu_perfil_6_titulo'] = config_parameter.get_param('app_menu_perfil_6_titulo')
        result['app_menu_perfil_6_url'] = config_parameter.get_param('app_menu_perfil_6_url')
        result['app_menu_perfil_6_sequence'] = config_parameter.get_param('app_menu_perfil_6_sequence')
        result['app_menu_separador_1'] = config_parameter.get_param('app_menu_separador_1')
        result['app_menu_separador_1_sequence'] = config_parameter.get_param('app_menu_separador_1_sequence')
        result['app_menu_separador_2'] = config_parameter.get_param('app_menu_separador_2')
        result['app_menu_separador_2_sequence'] = config_parameter.get_param('app_menu_separador_2_sequence')
        result['app_menu_separador_3'] = config_parameter.get_param('app_menu_separador_3')
        result['app_menu_separador_3_sequence'] = config_parameter.get_param('app_menu_separador_3_sequence')
        result['app_menu_separador_4'] = config_parameter.get_param('app_menu_separador_4')
        result['app_menu_separador_4_sequence'] = config_parameter.get_param('app_menu_separador_4_sequence')

        return result
