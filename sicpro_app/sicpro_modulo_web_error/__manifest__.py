# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Web Error',
    'version': '1.0', 'category': 'Administración',
    'summary': 'El modulo se encarga de las configuraciónes de los errores ('
               '403, 404, 405)', 'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        'nucleo_sicpro_erp',
        "base",
        "http_routing",
    ],

    "data": ['view/website_templates.xml'],

    "installable": True,
    'application': True,
    "auto_install": False,
}
