# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Solicitudes de Trabajo',
    'version': '1.0',
    'sequence': 2,
    'category': 'Solicitudes',
    'summary': "Esta aplicación se encargara de la recepción de "
               "solicitudes de trabajo y da inicio al proceso de ejecución.",
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'license': 'AGPL-3',
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        'calendar',
        'sicpro_app_clientes',
        'sicpro_app_trabajadores',
    ],
    'data': [
        'security/solicitudes.xml',
        'security/ir.model.access.csv',
        'views/solicitudes_estados_views.xml',
        'views/solicitudes_rechazo_views.xml',
        'views/solicitudes_etiquetas_views.xml',
        'data/rechazadas_data.xml',
        'data/plantillas_correo_data.xml',
        'data/etiquetas_data.xml',
        'data/estados_data.xml',
        'views/solicitudes_inversionistas_views.xml',
        'views/solicitudes_negociacion_views.xml',
        'views/solicitudes_negociacion_pg_views.xml',
        'views/solicitudes_ejecutor_views.xml',
        'views/solicitudes_grupos_views.xml',
        'views/solicitudes_tablasreportes_views.xml',
        'views/solicitudes_menu_views.xml',
    ],
    'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': True,
    'auto_install': False
}
