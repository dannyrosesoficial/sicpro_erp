# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Seguridad de Importación',
    'version': '1.0',
    'category': 'Administración',
    'summary': "Este módulo se encargar de controlar la seguridad para "
               "importar datos por los usuarios",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        "web",
        "base_import"
    ],
    'data': [
        "security/importar_security.xml",
        "views/base_import.xml",
    ],
    'installable': True,
    'application': True,
}
