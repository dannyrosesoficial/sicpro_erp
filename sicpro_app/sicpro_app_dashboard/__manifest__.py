# -*- coding: utf-8 -*-

{
    'name': 'Mi Dashboard Personal',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Producción',
    'sequence': 2,
    'summary': 'Dashboards personal del usuario',
    'description': "Método de visualización del usuario mediante el dashboard",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': ['base', 'web', 'nucleo_sicpro_erp'],
    'data': [
        'security/ir.model.access.csv',
        'views/board_views.xml',
        'views/ir_view_custom_view.xml',
        ],
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'sicpro_app_dashboard/static/src/**/*.scss',
            'sicpro_app_dashboard/static/src/**/*.js',
        ],
        'web.qunit_suite_tests': [
            'sicpro_app_dashboard/static/tests/**/*',
        ],
        'web.assets_qweb': [
            'sicpro_app_dashboard/static/src/**/*.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
