# -*- coding: utf-8 -*-

from . import models

# verífica la versión del sistema antes de instalar
def pre_init_check(cr):
    from odoo.service import common
    from odoo.exceptions import Warning
    version_info = common.exp_version()
    server_serie = version_info.get('server_serie')
    if server_serie != '15.0':
        raise Warning('El módulo es soportado solo por SICPROERP-Odoo versión 15.0, actualmente usa la:  {}.'.format(server_serie))
    return True
