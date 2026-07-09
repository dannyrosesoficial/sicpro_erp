# -*- coding: utf-8 -*-


{
    "name": "SICPRO: API Deck Nextcloud Reuniones",
    "summary": "Herramienta para la vinculación de los acuerdos de reuniones con la aplicación móvil Deck",
    "version": "1.0",
    "category": "Administración",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    "description": "Herramienta para la vinculación de los acuerdos de reuniones con la aplicación móvil Deck",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": ['base',
                'nucleo_sicpro_erp',
                'sicpro_app_nube_etecsa',
                'sicpro_app_reuniones',
                ],
    'data': [
        # 'data/plantillas_correo.xml',
        'views/res_users_views.xml',
    ],
    'assets': {
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
