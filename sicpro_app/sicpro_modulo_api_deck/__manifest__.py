# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: API Deck Nextcloud',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'category': 'Administración',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'LGPL-3',
    'sequence': 3,
    'summary': "Módulo base para la integración del sistema con el Deck de Nextcloud.",
    'description': "Módulo base para la integración del sistema con el Deck de Nextcloud.",
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'base',
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/administracion_rest_api_view.xml',
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
