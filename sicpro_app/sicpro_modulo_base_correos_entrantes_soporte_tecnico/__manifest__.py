# -*- coding: utf-8 -*-


{
    "name": "SICPRO: Base de Correos Entrantes - Soporte Técnico",
    "summary": "Se encarga de controlar y distribuir los correos de entrada de la aplicación de Soporte Técnico",
    "version": "1.0",
    "category": "Administración",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    "description": "Se encarga de controlar y distribuir los correos de entrada de la aplicación de Soporte Técnico",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": [
        'base',
        'fetchmail',
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'sicpro_modulo_base_correos_entrantes',
        'sicpro_app_soporte'
    ],
    'data': [],
    'assets': {
        'web.assets_qweb': [],
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
