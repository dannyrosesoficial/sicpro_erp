# -*- coding: utf-8 -*-

{
    'name': 'SICPRO - Personalización Avanzada',
    'version': '1.0',
    'author': 'Daniel Barrero Reyes',
    'category': 'Herramientas',
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    'license': 'LGPL-3',
    'sequence': 3,
    'summary': """Personalización del módulo SICPRO.""",
    'description': """Este módulo permite personalizar SICPRO ERP""",
    'images': [],
    'depends': [
        'base_setup',
        'web',
        'mail',
        'iap',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/app_odoo_customize_views.xml',
        'views/app_theme_config_settings_views.xml',
        'views/res_config_settings_views.xml',
        # data
        'data/ir_config_parameter.xml',
        'data/res_company_data.xml',
        'data/res_groups.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
