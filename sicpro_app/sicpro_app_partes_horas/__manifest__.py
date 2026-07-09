# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Partes de Horas',
    'version': '1.0',
    'category': 'Partes de Horas/Partes de Horas',
    'sequence': 2,
    'summary': "Esta aplicación se encargara del control de las horas "
               "empleadas por el trabajador",
    'description': "Modulo de partes de horas",
    'author': 'Daniel Barrero Reyes',
    'license': 'AGPL-3',
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    'depends': [
        'uom',
        'sicpro_app_trabajadores',
        'sicpro_app_preparacion_tecnica',
    ],
    'data': [
        'security/partes_horas.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/partes_horas_partes_views.xml',
        'views/partes_horas_views.xml',
        'views/partes_horas_preparaciones_views.xml',
        'views/partes_horas_trabajadores_views.xml',
        'views/partes_horas_temporizador_view.xml',
        'report/partes_horas_reportes_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
