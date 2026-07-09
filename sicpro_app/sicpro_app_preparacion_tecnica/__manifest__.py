# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Preparación Técnica',
    'version': '1.0',
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    'category': 'Preparación Técnica/SICPRO - APP: Preparación Tecnica',
    'sequence': 2,
    'summary': "Esta aplicación se encargara de la preparacion y puesta en "
               "marcha de la obra con la realización de la preparación técnica"
               " del trabajo.",
    'author': 'Daniel Barrero Reyes',
    'license': 'AGPL-3',
    'depends': [
        'base_setup',
        'mail',
        'portal',
        'rating',
        'resource',
        'web',
        'sicpro_app_trabajadores',
        'sicpro_app_clientes',
        'sicpro_app_materiales_insumos',
        'sicpro_app_transporte',

    ],
    'description': "Modulo de preparación técnica",
    'data': [
        'security/preparacion_tecnica.xml',
        'security/ir.model.access.csv',
        'views/preparacion_tecnica_anexoe_views.xml',
        'views/preparacion_tecnica_etiquetas_views.xml',
        'views/preparacion_tecnica_estados_views.xml',
        'views/preparacion_tecnica_preparaciones_views.xml',
        'views/preparacion_tecnica_ejecutores_views.xml',
        'views/preparacion_tecnica_actividades_views.xml',
        'views/preparacion_tecnica_assets.xml',
        'views/preparacion_tecnica_clasificacion_views.xml',
        'report/informe_preparacion_general_views.xml',
        'report/informe_preparacion_general_chatter_views.xml',
        'views/preparacion_tecnica_views.xml',
        'views/mail_activity_views.xml',

        # 'views/res_partner_views.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
