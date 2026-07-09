# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Tableau',
    'version': '1.0',
    'sequence': 2,
    'category': 'Aplicaciones',
    'summary': """Esta aplicación se encargara de la integración de las tablas
     asociadas con el sistema SICPRO ERP.""",
    'depends': ['base',
                'mail',
                'sicpro_app_trabajadores',
                'sicpro_app_contratos',
                ],
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'license': 'AGPL-3',
    'data': [
        'security/tableau.xml',
        'security/ir.model.access.csv',
        'views/tableau_views.xml',
        'data/tableau_data.xml',
        'views/tableau_menu_views.xml',
    ],
    'installable': True,
    'application': True,
}
