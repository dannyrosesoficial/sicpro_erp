# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    'name': 'SICPRO: Expande/Contrae grupos',
    'version': '19.0.0.0.1',
    'category': 'Técnico',
    'summary': 'Le permite expandir y contraer grupos creados y agrupar los'
               ' datos por un determinado campo para vistas de lista y kanban.',
    'description': 'Le permite expandir y contraer grupos creados y agrupar '
                   'los datos por un determinado campo para vistas de lista y kanban.',
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
        'web',
        'sicpro_app_administracion',
    ],
    "data": [],
    'assets': {
        'web.assets_backend': [
            '/sicpro_modulo_tema_agrupar/static/src/**/*',
        ],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}