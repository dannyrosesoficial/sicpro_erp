# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Conector Audio/Video',
    'version': '1.0',
    'category': 'Administración',
    'summary': 'Permite agregar formatos de audio y video en timpo'
               ' real mediante grabaciones',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        'nucleo_sicpro_erp',
        "base",
        'web_editor',
    ],
    "data": ['views/assets.xml'],

    "installable": True,
    'application': True,
    "auto_install": False,
}