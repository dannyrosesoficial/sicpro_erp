# -*- coding: utf-8 -*-


{
    "name": "SICPRO: API Calendario",
    "summary": "Herramienta para la vinculación del calendario mediante la tecnología caldav.",
    "version": "1.0",
    "category": "Administración",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    "description": "Herramienta para la vinculación del calendario mediante la tecnología caldav.",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": ['base',
                'sicpro_app_calendario',
                'calendar',
                'nucleo_sicpro_erp',
                'sicpro_app_administracion',
                'sicpro_app_nube_etecsa',
                ],
    'data': [
        'data/plantillas_correo.xml',
        'views/res_users_views.xml',
        'views/administracion_rest_api_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_modulo_api_calendario/static/src/js/caldav_calendario.js',
            'sicpro_modulo_api_calendario/static/src/scss/caldav_calendar.scss',
        ],
        'web.assets_qweb': [
            'sicpro_modulo_api_calendario/static/src/xml/base_calendario.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',,
}
