# -*- coding: utf-8 -*-


{
    "name": "SICPRO: Base de Correos Entrantes",
    "summary": "Se encarga de controlar y distribuir los correos de entrada a las aplicaciones del sistema SICPRO ERP.",
    "version": "1.0",
    "category": "Administración",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    "description": "Se encarga de controlar y distribuir los correos de entrada a las aplicaciones del "
                   "sistema SICPRO ERP.",
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
        'sicpro_app_administracion'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/metodos_correos_entrantes_views.xml',
        'views/fetchmail_views.xml',
        'views/metodos_correos_entrantes_menu_views.xml'
    ],
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
