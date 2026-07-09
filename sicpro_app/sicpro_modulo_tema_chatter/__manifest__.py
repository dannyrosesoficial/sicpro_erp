# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Chatter',
    'version': '19.0.0.0.1',
    'summary': "Permite seleccionar la posición donde desea el chatter.",
    'description': "Permite seleccionar la posición donde desea el chatter.",
    'category': 'Técnico',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        "base",
        "mail",
        'sicpro_app_administracion',
    ],
    "data": [
      'views/res_users_views.xml',
      'views/web.xml',
    ],
    "assets": {
        "web.assets_backend": [
            '/sicpro_modulo_tema_chatter/static/src/scss/chatter_custom.scss',
            '/sicpro_modulo_tema_chatter/static/src/js/web_chatter_position.esm.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
