# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Firma Digital',
    'version': '1.0',
    'summary': "Gestión de el proceso de firma digital",
    'description': "Aquí esta recogida la configuración de la firma digital "
                   "de los documentos",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': "https://www.facebook.com/danielbarreroreyes.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        'web'
    ],
    "data": [
        "views/web_digital_sign_view.xml",
        "views/users_view.xml"
    ],
    "qweb": ['static/src/xml/digital_sign.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}