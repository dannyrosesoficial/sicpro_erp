# -*- coding: utf-8 -*
from . import models


# verífica la versión del sistema antes de instalar
def pre_init_check(cr):
    from odoo.exceptions import UserError
    from odoo.release import series
    # series contiene la versión principal, ej: '15.0'
    server_serie = series

    if server_serie != '15.0':
        raise UserError('El módulo es soportado solo por SICPROERP-Odoo versión 15.0, actualmente usa la:  {}.'.format(
            server_serie))
    return True