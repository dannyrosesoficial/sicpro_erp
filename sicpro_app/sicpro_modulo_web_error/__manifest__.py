# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    'name': 'SICPRO: Web Error',
    'version': '19.0.0.0.1',
    'category': 'Website',
    'summary': 'El módulo se encarga de las configuraciones de los errores '
               '(400, 404, 403, 500)',
    'description': 'El módulo se encarga de las configuraciones de los errores '
               '(400, 404, 403, 500)',
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
        "http_routing",
        'sicpro_app_administracion',
    ],
    "data": [
        'view/templates.xml'
    ],
    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}
