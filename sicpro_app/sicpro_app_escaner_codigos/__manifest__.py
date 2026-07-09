# -*- coding: utf-8 -*-

{
    "name": "SICPRO: Escáner de Código de Barras/QR",
    "summary": "Módulo para agregar la función de escanear datos mediante el código de barras/QR",
    "version": "1.0",
    "category": "Administración",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    "description": "Módulo para agregar la función de escanear datos mediante el código de barras/QR",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/qr_scanner_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/sicpro_app_escaner_codigos/static/src/js/qr_scanner_pop_up.js',
            '/sicpro_app_escaner_codigos/static/src/scss/qr_code_scanner.scss',
            '/sicpro_app_escaner_codigos/static/src/scss/qr_scanner_pop_up.scss',
        ],
        'web.assets_qweb': [
            '/sicpro_app_escaner_codigos/static/src/xml/qr_scanner_pop_up.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
