# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Actualiza vistas List/Kanban',
    'version': '19.0.0.0.1',
    'category': 'Técnico',
    'summary': "Permite desde un botón actualizar los datos de las vistas"
               " de listas y kanban",
    'description': "Permite desde un botón actualizar los datos de las vistas"
                   " de listas y kanban",
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
    "data": [],
    "assets": {
        "web.assets_backend": [
            "sicpro_modulo_actualiza_list_kanban/static/src/scss/refresher.scss",
            "sicpro_modulo_actualiza_list_kanban/static/src/xml/refresher.xml",
            (
                "after",
                "web/static/src/search/control_panel/control_panel.js",
                "sicpro_modulo_actualiza_list_kanban/static/src/js/*.esm.js",
            ),
            (
                "after",
                "web/static/src/search/control_panel/control_panel.xml",
                "sicpro_modulo_actualiza_list_kanban/static/src/xml/control_panel.xml",
            ),
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
