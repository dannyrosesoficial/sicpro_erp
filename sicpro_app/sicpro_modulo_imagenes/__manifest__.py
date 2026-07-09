# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Trabajos con Imágenes',
    'version': '19.0.0.0.1',
    'category': 'Técnico',
    'summary': "Este módulo se encarga de expandir todo lo relacionado con"
               " las imágenes del sistema",
    'description': "Este módulo se encarga de expandir todo lo relacionado con"
                   " las imágenes del sistema",
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
        "web",
        'sicpro_app_administracion',
    ],
    "data": [],
    'assets': {
        'web.assets_backend': {
            'sicpro_modulo_imagenes/static/src/js/image_preview_widget.js',
            'sicpro_modulo_imagenes/static/src/xml/widget_image_preview.xml',
        }
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}