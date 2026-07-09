# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    'name': 'SICPRO: Timeout',
    'version': '19.0.0.0.1',
    'category': 'Técnico',
    'summary': 'El módulo se encarga de cerrar la session después del '
               'tiempo predeterminado por la configuración',
    'description': 'El módulo se encarga de cerrar la session después del'
                   ' tiempo predeterminado por la configuración',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        "base",
        "sicpro_app_administracion"
    ],
    "data": [
        "data/ir_config_parameter.xml"
    ],
    "assets": {
        "web.assets_backend": [],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}