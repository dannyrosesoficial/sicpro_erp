# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models
from odoo.http import request



class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        config_parameter = request.env['ir.config_parameter'].sudo()
        result['app_system_name'] = config_parameter.get_param('app_system_name', 'SICPRO ERP')
        result['app_documentation_url'] = config_parameter.get_param('app_documentation_url')
        result['app_documentation_dev_url'] = config_parameter.get_param('app_documentation_dev_url')
        result['app_support_url'] = config_parameter.get_param('app_support_url')
        result['app_account_title'] = config_parameter.get_param('app_account_title')
        result['app_account_url'] = config_parameter.get_param('app_account_url')
        result['app_show_lang'] = config_parameter.get_param('app_show_lang')
        result['app_show_debug'] = config_parameter.get_param('app_show_debug')
        result['app_show_documentation'] = config_parameter.get_param('app_show_documentation')
        result['app_show_documentation_dev'] = config_parameter.get_param('app_show_documentation_dev')
        result['app_show_support'] = config_parameter.get_param('app_show_support')
        result['app_show_account'] = config_parameter.get_param('app_show_account')
        result['app_show_poweredby'] = config_parameter.get_param('app_show_poweredby')
        result['app_lang_list'] = self.env['res.lang'].search_read([], ['id', 'code', 'name'])
        result['is_erp_manager'] = self.env.user.has_group('base.group_erp_manager')
        result['app_navbar_pos_pc'] = config_parameter.get_param('app_navbar_pos_pc', 'top')
        result['app_navbar_pos_mobile'] = config_parameter.get_param('app_navbar_pos_mobile', 'top')
        return result
