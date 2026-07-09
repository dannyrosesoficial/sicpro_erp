# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Expandir Grupos Vistas de Lista',
    'version': '19.0.0.0.1',
    'summary': "Este módulo se encarga de poder expandir los grupos en la "
               "vista de árbol o lista",
    'description': "Este módulo se encarga de poder expandir los grupos en la "
                   "vista de árbol o lista",
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
        "web",
        'sicpro_app_administracion',
    ],
    "assets": {
        "web.assets_backend": [
            "sicpro_modulo_groupby_expand_collapse/static/src/css/groupby_expand_collapse.css",
            "sicpro_modulo_groupby_expand_collapse/static/src/js/groupby_expand_collapse.js",
            "sicpro_modulo_groupby_expand_collapse/static/src/xml/expand_collapse_buttons.xml",
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
