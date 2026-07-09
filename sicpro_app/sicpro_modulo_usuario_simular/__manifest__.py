# -*- coding: utf-8 -*-

{
    "name": "SICPRO: Simulación de Usuarios",
    "summary": "Aplicación para simulación de sesión",
    "version": "1.0",
    "category": "Administración",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    "description": "Aplicación para simulación de sesión de los usuarios",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": [
        "base",
        "web",
        'nucleo_sicpro_erp',
        'sicpro_app_administracion'
    ],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "wizard/simular_usuario_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sicpro_modulo_usuario_simular/static/src/js/user_simulation.js",
        ],
        "web.assets_qweb": [
            "sicpro_modulo_usuario_simular/static/src/xml/widget.xml",
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}

