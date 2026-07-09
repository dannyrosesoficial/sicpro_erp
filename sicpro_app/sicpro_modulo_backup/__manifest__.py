# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Gestión de Backup',
    'version': '1.0',
    'summary': "Autobackup del sistema SICPRO ERP",
    'description': "Este módulo se encarga de generar las salvas progrmadas "
                   "del sistema",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': "https://www.facebook.com/danielbarreroreyes.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        #'sicpro_modulo_webdav',
        'sicpro_app_administracion'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/backup_view.xml',
        'data/cron_backup_data.xml',
        'data/email_data.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
