# -*- coding: utf-8 -*-


{
    "name": "SICPRO: Relación de Tema Visual con Login",
    "summary": "Vincula la acción del botón de iniciar sesión con el tema visual para que se ejecute la vista de menu",
    "version": "1.0",
    "category": "Administración",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    "description": "Vincula la acción del botón de iniciar sesión con el tema visual para que se "
                   "ejecute la vista de menu",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": [
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'sicpro_modulo_temavisual',
        'sicpro_modulo_web_login'
    ],
    "data": ['views/login_action_initial.xml'],
    'assets': {
        'web._assets_primary_variables': [],
        'web._assets_secondary_variables': [],
        'web.assets_backend': [],
        'web.assets_qweb': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}


