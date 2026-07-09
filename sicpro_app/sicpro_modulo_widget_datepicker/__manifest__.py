# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Multiples Fechas',
    'version': '19.0.0.0.1',
    'summary': "Permite la selección de multiples fechas en un solo campo y "
               "modificar la traducción de los meses, semanas y días del "
               "formato de calendario.",
    'description': "Permite la selección de multiples fechas en un solo campo "
                   "y modificar la traducción de los meses, semanas y días del"
                   " formato de calendario.",
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
    ],
    'data': [],
    'assets': {
        'web.assets_backend': {
            'sicpro_modulo_widget_datepicker/static/src/css/datepicker_widget.css',
            'sicpro_modulo_widget_datepicker/static/src/xml/datepicker_widget.xml',
            'sicpro_modulo_widget_datepicker/static/src/js/datepicker_widget.js',
        },
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
