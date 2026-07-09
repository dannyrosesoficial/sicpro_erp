# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import base64

from odoo.tools import file_open
from . import models


# verífica la versión del sistema antes de instalar
def pre_init_check(cr):
    from odoo.service import common
    from odoo.exceptions import UserError
    version_info = common.exp_version()
    server_serie = version_info.get('server_serie')
    if not server_serie or not server_serie.startswith('19.'):
        raise UserError(
            'El módulo está probado para Odoo 19.x. Versión detectada: %s' % (
                    server_serie or 'desconocida'))
    return True


def _setup_module(env):
    if env.ref('base.main_company', False):
        with file_open('sicpro_modulo_tema_visual/static/src/img/favicon.png',
                       'rb') as file:
            env.ref('base.main_company').write(
                {'favicon': base64.b64encode(file.read())})
        with file_open(
            'sicpro_modulo_tema_visual/static/src/img/background-dark.jpg',
            'rb') as file:
            image_data = base64.b64encode(file.read()).decode()

            env['ir.config_parameter'].sudo().set_param(
                'sicpro.theme_background_image', image_data)


def _uninstall_cleanup(env):
    env['res.config.settings']._reset_theme_color_assets()
