# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Trabajos con Imagenes',
    'version': '1.0',
    'category': 'Administración',
    'summary': "Este módulo se encargar de expandir todo lo relacionado "
               "a las imagenes del sistema",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        "web",
        "mail",
    ],
    "data": [
        "views/assets.xml",
        "views/swipe_images.xml",
    ],

    "qweb": [
        "static/src/xml/web_widget_image_webcam.xml",
        'static/src/xml/image.xml',
    ],
    'installable': True,
    'application': True,
}