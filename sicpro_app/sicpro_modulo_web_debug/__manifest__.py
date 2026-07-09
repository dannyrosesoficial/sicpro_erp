# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Web Debug',
    'version': '19.0.0.0.1',
    'summary': "Aplicación para entrar en el modo desarrollo de SICPRO ERP",
    'description': "Aplicación para entrar en el modo desarrollo de SICPRO ERP",
    'category': 'Website',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": ['web',
                'sicpro_app_administracion',
                ],
    'assets': {
        'web.assets_backend': [
            'sicpro_modulo_web_debug/static/src/js/web_debug.js',
            'sicpro_modulo_web_debug/static/src/xml/web_debug.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
