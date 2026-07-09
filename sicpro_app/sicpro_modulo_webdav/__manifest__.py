# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Conector Webdav',
    'version': '1.0',
    'category': 'Administración',
    'summary': 'Crear una nueva configuración para conexiones '
               'models con SICPRO ERP',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        'nucleo_sicpro_erp',
        "base",
    ],
    "data": [],

    "installable": True,
    'application': True,
    "auto_install": False,
}
