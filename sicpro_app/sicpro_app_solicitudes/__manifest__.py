# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Solicitudes',
    'version': '1.0',
    'sequence': 2,
    'category': 'Solicitudes/Solicitud',
    'summary': "Esta aplicación se encargara de la recepción de "
               "solicitudes de trabajo y da inicio al proceso de ejecución.",
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    'author': 'Daniel Barrero Reyes',
    'license': 'AGPL-3',
    'depends': ['sicpro_app_solicitudes_t1',
                'sicpro_app_solicitudes_t2',
                'sicpro_app_solicitudes_t3',
                'sicpro_app_solicitudes_t4',
                'sicpro_app_solicitudes_t5',
                'sicpro_app_solicitudes_t6',
                ],
    'data': [
    ],
    'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': True,
    'auto_install': False
}
