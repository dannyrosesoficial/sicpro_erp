# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Notificaciones Web',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Enviar mensajes de notificación al usuario.",
    'description': "Enviar mensajes de notificación al usuario.",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": ["web",
                "bus",
                "base",
                "mail",
                ],
    'data': [
        # solo se habilita para comprobar que ese funcionando.
        # 'views/res_users_notify_demo.xml'
    ],
    'assets': {
        'web.assets_backend': [
            "sicpro_modulo_web_notify/static/src/js/services/*.js",
        ],
        'web.assets_frontend': [],
        'web.assets_qweb': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}