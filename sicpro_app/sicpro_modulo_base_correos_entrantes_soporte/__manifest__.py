# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Solicitud de Correos desde Soporte',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': "Este módulo se encarga realizar la solicitud de correos entrantes desde la app de soporte",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': ['nucleo_sicpro_erp',
                'base',
                'fetchmail',
                'sicpro_app_administracion',
                'sicpro_modulo_base_correos_entrantes',
                'sicpro_app_soporte',
                ],
    'data': [
        'views/soporte_ticket_correos_view.xml',
    ],
    'assets': {
        'web.assets_backend': [],
        'web.qunit_suite_tests': [],
        'web.assets_qweb': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
