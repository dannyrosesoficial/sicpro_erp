# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Audio y Video',
    'version': '19.0.0.0.1',
    'summary': 'Agrega la función de incorporar archivos de audio y video al campo de html',
    'description': 'Agrega la función de incorporar archivos de audio y '
                   'video al campo de html',
    'category': 'Técnico',
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
        'html_editor',
        'sicpro_app_administracion',
    ],
    'data': [],
    'assets': {
        'html_editor.assets_editor': [
            'sicpro_modulo_audio_video/static/src/js/video_plugin.js',
            'sicpro_modulo_audio_video/static/src/js/audio_plugin.js',
        ],
        'html_editor.assets_media_dialog': [
            'sicpro_modulo_audio_video/static/src/js/video_dialog.js',
            'sicpro_modulo_audio_video/static/src/xml/video_dialog_template.xml',
            'sicpro_modulo_audio_video/static/src/js/audio_dialog.js',
            'sicpro_modulo_audio_video/static/src/xml/audio_dialog_template.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
