# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    'name': 'SICPRO: Colores',
    'version': '19.0.0.0.1',
    'category': 'Técnico',
    'summary': 'Personaliza los colores de SICPRO ERP',
    'description': 'Este módulo le ofrece opciones para personalizar los'
                   ' colores del tema.',
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
        'base_setup',
        'sicpro_app_administracion',
    ],
    'data': [
        'templates/webclient.xml',
        'views/res_config_settings.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('prepend', 'sicpro_modulo_tema_colores/static/src/scss/colors.scss'),
            (
                'before',
                'sicpro_modulo_tema_colores/static/src/scss/colors.scss',
                'sicpro_modulo_tema_colores/static/src/scss/colors_light.scss'
            ),
        ],
        'web.assets_web_dark': [
            (
                'after',
                'sicpro_modulo_tema_colores/static/src/scss/colors.scss',
                'sicpro_modulo_tema_colores/static/src/scss/colors_dark.scss'
            ),
        ],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}