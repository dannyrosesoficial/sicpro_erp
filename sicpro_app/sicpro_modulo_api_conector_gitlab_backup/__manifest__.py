# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: API Conector (BACKUP)',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': "Este módulo se encarga de sincronizar los backups del sistema con la nube de salva Gitlab",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "external_dependencies": {"python": ["GitPython"]},
    'depends': ['nucleo_sicpro_erp',
                'base',
                'sicpro_app_administracion',
                'sicpro_modulo_api_conector',
                ],
    'data': [
        'views/conector_rest_api_views.xml',
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
