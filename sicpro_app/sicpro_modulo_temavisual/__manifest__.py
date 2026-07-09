# -*- coding: utf-8 -*-

{
    "name": "SICPRO: Tema Visual SICPRO ERP",
    "summary": "Tema para la plataforma SICPRO ERP",
    "version": "1.0",
    "category": "Administración",
    "website": 'https://www.facebook.com/danielbarreroreyes.oficial/',
    "description": """Tema Backend para la aplicación SICPRO ERP""",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'license': 'LGPL-3',
    'sequence': 3,

    "depends": [
        'nucleo_sicpro_erp',
        'base',
        'web',
        #'ow_web_responsive',
        'sublime_web_responsive',
    ],
    "data": [
        'views/assets.xml',
        'views/res_company_view.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
