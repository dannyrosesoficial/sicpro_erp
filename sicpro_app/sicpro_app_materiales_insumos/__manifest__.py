# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Materiales e Insumos',
    'version': '1.0',
    'category': 'Materiales e Insumos/Materiales e Insumos',
    'summary': "Esta aplicación le ofrece un control de los "
               "Materiales e Insumos que se utilizan en los procesos.",
    'author': 'Daniel Barrero Reyes',
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    'license': 'AGPL-3',
    'sequence': 2,
    'depends': ['base', 'sicpro_modulo_nomencladores', 'mail', ],

    'data': [
        'security/productos.xml',
        'security/ir.model.access.csv',
        'views/productos_views.xml',
        'views/productos_materiales_insumos_views.xml',
        'views/productos_etiquetas_views.xml',
        'views/productos_um_views.xml',
    ],
    'installable': True,
    'application': True,
}
