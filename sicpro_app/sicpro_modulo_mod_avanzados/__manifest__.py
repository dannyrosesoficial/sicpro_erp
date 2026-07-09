# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Personalización Avanzada',
    'version': '19.0.0.0.1',
    'summary': "Este módulo permite personalizar SICPRO ERP.",
    'description': "Este módulo permite personalizar SICPRO ERP",
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
     'price': 0,
     'currency': 'CUP',
     'company': 'División de Proyectos y Ejecución de Obras',
     'category': 'Técnico',
     'website': 'https://www.facebook.com/dannyroses.oficial/',
     'license': 'LGPL-3',
     'sequence': 3,
    'depends': [
        'base_setup',
        'base_import',
        'base_import_module',
        'mail',
        'sicpro_app_administracion',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_config_parameter.xml',
        'data/res_company.xml',
        'views/app_odoo_customize_views.xml',
        'views/res_config_settings_views.xml',
        'views/ir_views.xml',
        'views/ir_actions_act_window_views.xml',
        'views/ir_module_addons_path_views.xml',
        'views/ir_module_module_views.xml',
        'views/ir_module_category_views.xml',
        'views/ir_sequence_views.xml',
        'views/ir_ui_menu_views.xml',
        'views/ir_ui_view_views.xml',
        'views/ir_model_data_views.xml',
        'views/ir_model_fields_views.xml',
        'views/ir_model_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_modulo_mod_avanzados/static/src/scss/app.scss',
            'sicpro_modulo_mod_avanzados/static/src/scss/ribbon.scss',
            'sicpro_modulo_mod_avanzados/static/src/scss/dialog.scss',
            'sicpro_modulo_mod_avanzados/static/src/js/user_menu.js',
            'sicpro_modulo_mod_avanzados/static/src/js/ribbon.js',
            'sicpro_modulo_mod_avanzados/static/src/js/dialog.js',
            'sicpro_modulo_mod_avanzados/static/src/js/navbar.js',
            'sicpro_modulo_mod_avanzados/static/src/js/base_import_list_renderer.js',
            'sicpro_modulo_mod_avanzados/static/src/js/base_import_list_renderer.js',
            'sicpro_modulo_mod_avanzados/static/src/webclient/*.js',
            'sicpro_modulo_mod_avanzados/static/src/webclient/user_menu.xml',
            'sicpro_modulo_mod_avanzados/static/src/xml/res_config_edition.xml',
            'sicpro_modulo_mod_avanzados/static/src/xml/debug_templates.xml',
        ],
    },
     'installable': True,
     'application': True,
     'auto_install': False,
     'pre_init_hook': 'pre_init_check',
}
