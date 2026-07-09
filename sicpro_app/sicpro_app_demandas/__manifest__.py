# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Demandas',
    'version': '1.0',
    'sequence': 2,
    'category': 'Producción',
    'summary': "Demandas de artículos",
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'license': 'AGPL-3',
    'description': "Esta aplicación se encargará de todo el control la demanda"
                   " de articulos de la división",
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        'mail',
        'sicpro_app_administracion',
    ],
    'data': [
        'security/demandas.xml',
        'security/ir.model.access.csv',
        'views/demandas_etiquetas_views.xml',
        'views/demandas_catalogo_views.xml',
        'views/demandas_menu_views.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
