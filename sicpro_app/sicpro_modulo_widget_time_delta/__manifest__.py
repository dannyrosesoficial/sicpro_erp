# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Formato a Fechas',
    'version': '19.0.0.0.1',
    'summary': "Permite agregar nuevo estilo de formato a las fechas",
    "description": "Permite agregar nuevo estilo de formato a las fechas",
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
        'base',
        'web',
    ],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'sicpro_modulo_widget_time_delta/static/src/js/timedelta_field.js',
            'sicpro_modulo_widget_time_delta/static/src/js/timedelta_field.xml',
            'sicpro_modulo_widget_time_delta/static/src/css/timedelta_field.css',
            'sicpro_modulo_widget_time_delta/static/src/lib/jquery.js',
            'sicpro_modulo_widget_time_delta/static/src/lib/duration-picker/jquery-duration-picker.css',
            'sicpro_modulo_widget_time_delta/static/src/lib/duration-humanize/humanize-duration.js',
            'sicpro_modulo_widget_time_delta/static/src/lib/duration-picker/jquery-duration-picker.js',
            "sicpro_modulo_widget_time_delta/static/src/xml/qweb_template.xml",
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
