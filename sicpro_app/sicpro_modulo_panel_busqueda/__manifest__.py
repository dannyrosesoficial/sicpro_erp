# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    "name": "SICPRO: Barra Lateral de Búsqueda", 'version': '19.0.0.0.1',
    "category": "Técnico",
    "summary": "Barra Lateral de Búsqueda",
    "description": "Barra Lateral de Búsqueda",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": [
        'base',
        'web',
        'sicpro_app_administracion',
    ],
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
        'web.assets_backend': [
            'sicpro_modulo_panel_busqueda/static/src/css/search_panel_toggle.scss',
            'sicpro_modulo_panel_busqueda/static/src/js/search_panel_toggle.js',
            'sicpro_modulo_panel_busqueda/static/src/xml/search_panel_toggle.xml'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
