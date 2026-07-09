# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Vista FullScreen',
    'version': '19.0.0.0.1',
    'summary': "Permite la visualización del sistema en el navegador a pantalla completa",
    'description': "Permite la visualización del sistema en el navegador a pantalla completa",
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
    'depends': [
        'base',
        'sicpro_app_administracion'
    ],
    'data': [],
    "assets": {
        'web.assets_backend': {
            'sicpro_modulo_fullscreen/static/src/xml/sicpro_modulo_fullscreen.xml',
            'sicpro_modulo_fullscreen/static/src/js/sicpro_modulo_fullscreen.js',
        },
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
