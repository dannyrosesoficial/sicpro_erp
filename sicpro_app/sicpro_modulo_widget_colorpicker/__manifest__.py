# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Widget Color Picker',
    'version': '19.0.0.0.1',
    'summary': "Permite agregar nuevo widget de color a la vista.",
    "description": "Permite agregar nuevo widget de color a la vista.",
    'category': 'Técnico',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0, 'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
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
            'sicpro_modulo_widget_colorpicker/static/src/lib/pickr/classic.min.css',
            'sicpro_modulo_widget_colorpicker/static/src/lib/pickr/pickr.min.js',
            'sicpro_modulo_widget_colorpicker/static/src/css/widget.css',
            'sicpro_modulo_widget_colorpicker/static/src/js/color_picker_field.xml',
            'sicpro_modulo_widget_colorpicker/static/src/js/color_picker_field.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
