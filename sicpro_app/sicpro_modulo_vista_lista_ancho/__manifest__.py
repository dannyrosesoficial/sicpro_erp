# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Ancho de Columnas',
    'version': '19.0.0.0.1',
    'summary': "Permite recordar el ancho que se le da a las columnas"
               " en la vista de lista",
    'description': "Permite recordar el ancho que se le da a las columnas"
                   " en la vista de lista",
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
        'web',
        'sicpro_app_administracion',
    ],
    'data': [],
    "assets": {
        "web.assets_backend": [
            "sicpro_modulo_vista_lista_ancho/static/src/js/list_renderer.esm.js",
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
