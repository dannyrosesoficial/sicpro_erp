# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Seguridad de Importación',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': "Este módulo se encargará de controlar la seguridad para importar datos por los usuarios",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'base',
        "web",
        "base_import"
    ],
    'data': [
        "security/importar_security.xml",
        # "views/base_import.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_modulo_importar_seguridad/static/src/js/import.js'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
