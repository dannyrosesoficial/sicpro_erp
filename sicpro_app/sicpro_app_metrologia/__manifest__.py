# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Metrología',
    'version': '1.0',
    'sequence': 2,
    'category': 'Metrología/SICPRO - APP: Metrología',
    'summary': "Esta aplicación se encargara de todo el control de los "
               "instrumentos de medición de la división.",
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    'author': 'Daniel Barrero Reyes',
    'license': 'AGPL-3',
    'depends': ['base',
                'sicpro_modulo_nomencladores',
                'mail',
                'sicpro_app_trabajadores'],
    'data': [
        'security/metrologia.xml',
        'security/ir.model.access.csv',
        'data/mail_data.xml',
        'views/metrologia_views.xml',
        'views/metrologia_templates.xml',
        'views/mail_activity_views.xml',
        'views/trabajadores_rel.xml',
    ],
    'installable': True,
    'application': True,
}
