# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    "name": "SICPRO: Importar Aplicaciones",
    "summary": "Permite instalar módulos de SICPRO ERP directamente desde un "
               "archivo ZIP a través de la interfaz de usuario.",
    "description": "Permite instalar módulos de SICPRO ERP directamente desde un "
               "archivo ZIP a través de la interfaz de usuario.",
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
        'web',
        'sicpro_app_administracion',
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/addon_import.xml",
        "views/apps.xml",
    ],
    "assets": {
        "web.assets_backend": []
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}

