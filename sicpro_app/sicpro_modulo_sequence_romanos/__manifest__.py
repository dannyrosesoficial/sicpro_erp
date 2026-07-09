# -*- coding: utf-8 -*-

{
    "name": "SICPRO: Sequence Romanos",
    "summary": "Aplicación agregar números romanos a la secuencias automatizadas",
    "version": "1.0",
    "category": "Administración",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    "description": "Aplicación agregar números romanos a la secuencias automatizadas",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": [
        "base",
        'nucleo_sicpro_erp',
    ],
    'data': [
        'views/sequence_view.xml',
    ],
    "assets": {
        "web.assets_backend": [],
        "web.assets_qweb": [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
