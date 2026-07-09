# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Widget de Audio',
    'version': '19.0.0.1',
    'summary': "Permite la reproducción de audio en el sistema",
    'description': "Permite la reproducción de audio en el sistema",
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
        'sicpro_app_administracion',
        'web',
    ],
    'data': [],
    'assets': {
            'web.assets_backend': [
                'sicpro_modulo_widget_audio/static/src/xml/ks_audio.xml',
                'sicpro_modulo_widget_audio/static/src/css/ks_audio.css',
                'sicpro_modulo_widget_audio/static/src/js/ks_audio.js',
            ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
