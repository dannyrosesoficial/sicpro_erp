# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Registros de Usuario',
    'version': '1.0',
    'summary': "Detalles del usuario de inicio de sesión y dirección IP",
    'description': "Este módulo registra la información de inicio de sesión del usuario",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': "https://www.facebook.com/danielbarreroreyes.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        'web',
        'sicpro_app_administracion'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/registro_usuarios_views.xml',
        'views/registro_ips_view.xml',
        ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
