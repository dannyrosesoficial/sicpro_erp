# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Clientes',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Clientes',
    'summary': "Esta aplicación le ofrece una vista rápida de su directorio "
               "de clientes, accesible desde su página de inicio.",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 2,
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        'sicpro_modulo_nomencladores',
        'mail',
        'sicpro_app_contactos',
    ],

    'data': [
        'security/clientes_security.xml',
        'security/ir.model.access.csv',
        'views/clientes_views.xml',
        'views/clientes_etiquetas_views.xml',
        'views/res_user.xml',
        'data/etiquetas_data.xml',
        'views/clientes_menu_views.xml',
    ],
    'assets': {'web.assets_backend': [],
               'web.assets_qweb': [],
               },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
