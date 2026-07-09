# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Materiales e Insumos',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Productividad',
    'summary': "Esta aplicación le ofrece un control de los "
               "Materiales e Insumos que se utilizan en los procesos.",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 2,
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
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
    'assets': {
        'web.assets_backend': [],
        'web.assets_qweb': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
