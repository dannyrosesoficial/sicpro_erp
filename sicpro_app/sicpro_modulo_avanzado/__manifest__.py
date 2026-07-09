# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Personalización Avanzada',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'category': 'Administración',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'LGPL-3',
    'sequence': 3,
    'summary': "Personalización del módulo SICPRO.",
    'description': "Este módulo permite personalizar SICPRO ERP",
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        'base_setup',
        'web',
        'mail',
        'iap',
        'sicpro_app_administracion',
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/app_theme_config_settings_views.xml',
        'views/res_config_settings_views.xml',
        'views/ir_views.xml',
        'views/ir_module_module_views.xml',
        'views/ir_translation_views.xml',
        'views/ir_ui_menu_views.xml',
        'views/ir_ui_view_views.xml',
        'views/ir_model_fields_views.xml',
        'views/ir_model_data_views.xml',
        'views/webclient_templates.xml',
        # data
        'data/ir_config_parameter_data.xml',
        'data/res_company_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_modulo_avanzado/static/src/scss/app.scss',
            'sicpro_modulo_avanzado/static/src/scss/ribbon.scss',
            'sicpro_modulo_avanzado/static/src/scss/dialog.scss',
            'sicpro_modulo_avanzado/static/src/js/app_window_title.js',
            'sicpro_modulo_avanzado/static/src/js/ribbon.js',
            'sicpro_modulo_avanzado/static/src/js/dialog.js',
            'sicpro_modulo_avanzado/static/src/js/user_menu.js',
        ],
        'web.assets_qweb': [
            'sicpro_modulo_avanzado/static/src/xml/res_config_edition.xml'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
