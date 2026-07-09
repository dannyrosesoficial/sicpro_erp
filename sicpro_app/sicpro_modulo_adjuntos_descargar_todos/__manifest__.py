## -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Descargar adjuntos como ZIP',
    'version': '19.0.0.0.1',
    'category': 'Técnico',
    'summary': "Descargue todos los archivos adjuntos como un único archivo ZIP"
               " desde cualquier modelo directamente desde la vista de lista",
    'description': "Descargue todos los archivos adjuntos como un único archivo"
                   " ZIP desde cualquier modelo directamente desde la vista "
                   "de lista",
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'base',
        'web',
        'sicpro_app_administracion',
                ],
    'data': [],
    'assets': {
        'web.assets_backend': [
            '/sicpro_modulo_adjuntos_descargar_todos/static/src/list_controller.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
