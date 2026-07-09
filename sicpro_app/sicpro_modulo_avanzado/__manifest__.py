# -*- coding: utf-8 -*-


{
    'name': 'SICPRO - Personalización Avanzada',
    'version': '1.0',
    'author': 'Daniel Barrero Reyes',
    'category': 'Administración',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'LGPL-3',
    'sequence': 3,
    'summary': """Personalización del módulo SICPRO.""",
    'description': """Este módulo permite personalizar SICPRO ERP""",
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
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/app_odoo_customize_views.xml',
        'views/app_theme_config_settings_views.xml',
        'views/res_config_settings_views.xml',
        'views/ir_views.xml',
        'views/ir_module_module_views.xml',
        'views/ir_translation_views.xml',
        'views/ir_ui_menu_views.xml',
        'views/ir_ui_view_views.xml',
        'views/ir_model_fields_views.xml',
        "views/webclient_templates.xml",
        # data
        'data/ir_config_parameter_data.xml',
        'data/res_company_data.xml',
    ],
    'qweb': [
        'static/src/xml/customize_user_menu.xml',
        'static/src/xml/res_config_edition.xml',
    ],
    # 'pre_init_hook': 'pre_init_hook',
    # 'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': True,
    'auto_install': False,
}
