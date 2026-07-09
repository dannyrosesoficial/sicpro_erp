# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    'name': 'SICPRO: Cuadros de diálogos Wizard',
    'version': '19.0.0.0.1',
    'category': 'Técnico',
    'summary': 'Agrega opciones para los diálogos.',
    'description': 'Este módulo agrega una opción a los cuadros de diálogo '
                   'para expandirlos al modo de pantalla completa.'
                   'Cada usuario puede consultar el estado inicial de los '
                   'diálogos en sus preferencias.',
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
        'web',
        'sicpro_app_administracion',
    ],
    'data': [
        'views/res_users.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            (
                'after',
                'web/static/src/scss/primary_variables.scss',
                'sicpro_modulo_tema_dialogos/static/src/scss/variables.scss'
            ),
        ],
        'web.assets_backend': [
            (
                'after',
                'web/static/src/core/dialog/dialog.js',
                '/sicpro_modulo_tema_dialogos/static/src/core/dialog/dialog.js',
            ),
            (
                'after',
                'web/static/src/core/dialog/dialog.scss',
                '/sicpro_modulo_tema_dialogos/static/src/core/dialog/dialog.scss',
            ),
            (
                'after',
                'web/static/src/core/dialog/dialog.xml',
                '/sicpro_modulo_tema_dialogos/static/src/core/dialog/dialog.xml',
            ),
            (
                'after',
                'web/static/src/views/view_dialogs/select_create_dialog.js',
                '/sicpro_modulo_tema_dialogos/static/src/views/view_dialogs/select_create_dialog.js',
            ),
        ],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}