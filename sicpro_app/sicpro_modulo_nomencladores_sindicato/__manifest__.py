# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Nomenclador del sindicato',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'sequence': 3,
    'category': 'Administración',
    'summary': "Este módulo agrega todas las bases del nomenclador de las secciones sindicales de la DVPE",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'license': 'AGPL-3',
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': ['nucleo_sicpro_erp',
                'base',
                'sicpro_app_administracion',
                'sicpro_app_trabajadores',
                'sicpro_modulo_nomencladores',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/sindicato_views.xml',
        'views/trabajadores_areas_views.xml',
        'views/trabajadores_views.xml',
        'views/nomencladores_menu_views.xml'
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
