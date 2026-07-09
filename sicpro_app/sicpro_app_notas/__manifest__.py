# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Tablero de Notas',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'sequence': 2,
    'category': 'Productividad',
    'summary': "Esta aplicación se encargará de la gestión y productividad mediantes notas y recordatorios.",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'description': "Esta aplicación se encargará de la gestión y productividad mediantes notas y recordatorios.",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'license': 'AGPL-3',
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': ['nucleo_sicpro_erp',
                'base',
                'mail',
                'note',
                ],
    'data': [
        'security/note_security.xml',
        'security/ir.model.access.csv',
        'views/note_views.xml',
        'views/note_stage_views.xml',
        'views/note_tag_views.xml',
        'views/note_tableros_views.xml'
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


