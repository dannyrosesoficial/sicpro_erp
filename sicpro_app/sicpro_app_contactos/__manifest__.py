# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Contactos',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Visualización de los contactos del sistema",
    'description': "Aquí están recogidos todos los usuarios y contactos extras de la división",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'contacts',
        'base', 'mail',
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'sicpro_app_trabajadores',
        'sicpro_modulo_dashboard_extendido',
    ],
    "data": [
        # 'views/contactos_views.xml',
        'views/contactos_trabajadores_views.xml',
        'views/contactos_menu_views.xml',
    ],
    'assets': {
        'web.assets_qweb': [],
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
