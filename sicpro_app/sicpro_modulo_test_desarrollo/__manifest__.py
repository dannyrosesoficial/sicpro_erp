# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    "name": "SICPRO: Test para Desarrollo",
    'version': '19.0.0.0.1',
    "category": "Técnico",
    "summary": "Módulo para facilitar la prueba de funciones",
    "description": "Módulo para facilitar la prueba de funciones",
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
        'sicpro_app_administracion',
        # 'calendar',
        # 'sicpro_app_soporte',
        # 'sicpro_modulo_web_registro',
        # 'sicpro_modulo_ldap_query',
        # 'sicpro_app_clientes',
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        'views/test_views.xml',
        'views/test_excepciones_view.xml',
    ],
    "assets": {
        "web.assets_backend": [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}

