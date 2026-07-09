# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Transporte',
    'version': '1.0',
    'sequence': 2,
    'category': 'Transporte/SICPRO - APP: Transporte',
    'summary': "Esta aplicación se encargara de todo el control del parqué "
               "automotor de la división.",
    'depends': ['base', 'mail',
                'sicpro_modulo_nomencladores',
                'sicpro_app_trabajadores',
                ],
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    'author': 'Daniel Barrero Reyes',
    'license': 'AGPL-3',
    'data': [
        'security/transporte.xml',
        'security/ir.model.access.csv',
        'views/transporte_modelo_views.xml',
        'views/transporte_views.xml',
        'views/transporte_costo_views.xml',
        'views/transporte_board_view.xml',
        'views/mail_activity_views.xml',
        'data/fleet_cars_data.xml',
        'data/mail_data.xml',
        'views/transporte_trabajadores_rel.xml',
    ],
    'installable': True,
    'application': True,
}
