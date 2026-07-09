# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Servidor Info',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': "Módulo para controlar los principales parámetros de uso del servidor del sistema SICPRO ERP",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    'external_dependencies': {"python": ["psutil"]},
    'depends': ['nucleo_sicpro_erp',
                'base',
                'sicpro_app_administracion',
                ],
    'data': [
        #'data/settings_records.xml',
        'views/fields.xml',
    ],
    'assets': {
        'web.assets_backend': [
             'sicpro_modulo_servidor_info/static/js/auto_update.js',
        ],
        'web.qunit_suite_tests': [],
        'web.assets_qweb': [
            # '/sicpro_modulo_servidor_info/static/xml/auto_update.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
