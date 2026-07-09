# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    "name": "SICPRO: Usuario LDAP a Cliente local",
    "summary": "Aplicación para crear los clientes directamente desde él "
               "LDAP empresarial.",
    "description": "Aplicación para crear los clientes directamente desde él "
                   "LDAP empresarial.",
    'version': '19.0.0.0.1',
    "category": "Técnico",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": [
        "base",
        'sicpro_modulo_ldap_query',
        'sicpro_app_clientes',
        'sicpro_app_administracion',
    ],
    "data": [
        "views/clientes_views.xml",
    ],
    "assets": {
        "web.assets_backend": [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}

