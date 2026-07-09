# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    'name': 'SICPRO: Barra de aplicaciones',
    'version': '19.0.0.0.1',
    'category': 'Técnico',
    'summary': 'Agrega una barra lateral a la pantalla principal.',
    'description': 'Este módulo agrega una barra lateral a la pantalla principal. La barra lateral tiene una lista'
                   'de todas las aplicaciones instaladas.',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'base',
        'base_setup',
        'web',
        'sicpro_app_administracion',
    ],
    'data': [
        'templates/webclient.xml',
        'views/res_users.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'sicpro_modulo_tema_barra/static/src/scss/variables.scss',
        ],
        'web._assets_backend_helpers': [
            'sicpro_modulo_tema_barra/static/src/scss/mixins.scss',
        ],
        'web.assets_web_dark': [
            (
                'after', 'sicpro_modulo_tema_barra/static/src/scss/variables.scss',
                'sicpro_modulo_tema_barra/static/src/scss/variables.dark.scss',
             ),
        ],
        'web.assets_backend': [
            (
                'after', 'web/static/src/webclient/webclient.js',
                'sicpro_modulo_tema_barra/static/src/webclient/webclient.js',
             ),
            (
                'after', 'web/static/src/webclient/webclient.xml',
                'sicpro_modulo_tema_barra/static/src/webclient/webclient.xml',
            ),
            (
                'after', 'web/static/src/webclient/webclient.js',
                'sicpro_modulo_tema_barra/static/src/webclient/menus/app_menu_service.js',
            ),
            (
                'after', 'web/static/src/webclient/webclient.js',
                'sicpro_modulo_tema_barra/static/src/webclient/appsbar/appsbar.js',
            ),
            'sicpro_modulo_tema_barra/static/src/webclient/webclient.scss',
            'sicpro_modulo_tema_barra/static/src/webclient/appsbar/appsbar.xml',
            'sicpro_modulo_tema_barra/static/src/webclient/appsbar/appsbar.scss',
        ],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}