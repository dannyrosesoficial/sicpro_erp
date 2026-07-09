# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Salón de Clases',
    'version': '1.0',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'category': 'Productividad',
    'sequence': 2,
    'summary': "Esta aplicación se encargara de la preparación de los usuarios"
               " mediante de diversos temas de interés."
               " del trabajo.",
    'description': "Modulo de Salón de clases",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'license': 'AGPL-3',
    'depends': [
        'web',
        'base',
        'mail',
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
    ],
    'data': [
        'security/salon_clases.xml',
        'security/ir.model.access.csv',
        'views/salon_clases_etiquetas_views.xml',
        'views/salon_clases_tipo_views.xml',
        'views/salon_clases_views.xml',
        'views/salon_clases_temas_views.xml',
        'views/salon_clases_menu_views.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
