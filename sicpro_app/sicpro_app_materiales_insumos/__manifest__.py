# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Materiales e Insumos',
    'version': '1.0',
    'category': 'Productividad',
    'summary': "Esta aplicación le ofrece un control de los "
               "Materiales e Insumos que se utilizan en los procesos.",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 2,
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        'mail',
        'sicpro_modulo_nomencladores',
    ],

    'data': [
        'security/productos.xml',
        'security/ir.model.access.csv',
        'views/productos_views.xml',
        'views/productos_materiales_insumos_views.xml',
        'views/productos_etiquetas_views.xml',
        'views/productos_um_views.xml',
        'data/etiquetas_data.xml',
        'data/um_data.xml',
    ],

    'installable': True,
    'application': True,
}
