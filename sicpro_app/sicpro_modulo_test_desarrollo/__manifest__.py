# -*- coding: utf-8 -*-


{
    "name": "SICPRO: Test para Desarrollo",
    "summary": "Módulo para facilitar la prueba de funciones",
    "version": "1.0",
    "category": "Administración",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    "description": "Módulo para facilitar la prueba de funciones",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": [
        'nucleo_sicpro_erp',
        "base",
        'sicpro_app_administracion',
        'calendar',
        'sicpro_app_soporte',
        'sicpro_modulo_ldap_query',
        'sicpro_app_clientes',
        'sicpro_modulo_backup_server',
        'sicpro_modulo_certificados_digitales'
    ],
    "data": [
        "security/test.xml",
        "security/ir.model.access.csv",
        'views/test_views.xml',
        'views/test_excepciones_view.xml',
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
    # 'uninstall_hook': 'uninstall_hook',,
}

