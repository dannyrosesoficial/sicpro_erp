# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from . import models
from . import wizard

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
