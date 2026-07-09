# -*- coding: utf-8 -*-


{
    "name": "SICPRO: Barra Lateral de Búsqueda",
    "summary": "Barra Lateral de Búsqueda",
    "version": "1.0",
    "category": "Administración",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    "description": "Barra Lateral de Búsqueda de las vistas base",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": ['base', 'web', 'nucleo_sicpro_erp'],

    'data': [
        'views/res_groups_views.xml',
        'views/ir_actions_act_window_views.xml',
        'views/ir_actions_actions_views.xml',
        'views/ir_actions_report_views.xml',
        'views/ir_actions_server_views.xml',
        'views/ir_attachment_views.xml',
        'views/ir_default_views.xml',
        'views/ir_model_access_views.xml',
        'views/ir_model_constraint_views.xml',
        'views/ir_model_fields_views.xml',
        'views/ir_ui_menu_views.xml',
        'views/ir_ui_view_views.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'sicpro_modulo_barra_lateral/static/src/**/*.xml'
        ],
        'web.assets_backend': [
            'sicpro_modulo_barra_lateral/static/src/css/search_panel_toggle.scss',
            'sicpro_modulo_barra_lateral/static/src/js/search_panel_toggle.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
