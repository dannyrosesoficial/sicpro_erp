# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Solicitudes T6 - Tablas & Reportes',
    'version': '1.0',
    'sequence': 2,
    'category': 'Solicitudes/Tablas & Reportes',
    'summary': "Esta aplicación se encargara de la recepción de solicitudes "
               "de trabajo y da inicio al proceso de ejecución.",
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    'author': 'Daniel Barrero Reyes',
    'license': 'AGPL-3',
    'depends': ['sicpro_app_solicitudes_t1', ],
    'data': [
        'security/TablasReportes.xml',
        'security/ir.model.access.csv',
        'views/solicitudes_tablasreportes_views.xml',
    ],

    'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': False,
    'auto_install': False
}
