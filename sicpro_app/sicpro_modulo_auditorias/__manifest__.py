# -*- coding: utf-8 -*-

{
    'name': 'SICPRO - Registros de Auditoria',
    'version': '1.0',
    'category': 'Administración',
    'summary': """Este módulo se encargara de auditar todas las acciones de 
    la aplicación.""",
    'author': 'Daniel Barrero Reyes',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        'sicpro_app_administracion',
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "views/auditlog_view.xml",
        "views/http_session_view.xml",
        "views/http_request_view.xml",
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
