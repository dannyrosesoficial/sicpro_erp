# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import os
import logging
from os.path import join as opj


MANIFEST_NAMES = ("__manifest__.py", "__openerp__.py")
_logger = logging.getLogger(__name__)


def get_tmp_folder_modules(tmp_module_path="."):
    """Devuelve la lista de nombres de módulos"""

    def listdir(dir):
        def clean(name):
            name = os.path.basename(name)
            if name[-4:] == ".zip":
                name = name[:-4]
            return name

        def is_really_module(name):
            for mname in MANIFEST_NAMES:
                if os.path.isfile(opj(dir, name, mname)):
                    return True

        return [clean(it) for it in os.listdir(dir) if is_really_module(it)]

    plist = []
    for ad in [tmp_module_path]:
        if not os.path.exists(ad):
            _logger.warning("la ruta de complementos no existe: %s", ad)
            continue
        plist.extend(listdir(ad))
    return sorted(set(plist))
