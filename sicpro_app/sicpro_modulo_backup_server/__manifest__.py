# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    'name': 'SICPRO: Backup Server Local y Remoto',
    'version': '19.0.0.0.1',
    'summary': "Este módulo se encarga de generar las salvas programadas del sistema en el propio servidor",
    'description': "Este módulo se encarga de generar las salvas programadas del sistema en el propio servidor",
    'category': 'Técnico',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    "external_dependencies":  {
        'python': [
            'python-crontab', 'psycopg2', 'paramiko'
        ]},
    "depends":  [
        'base',
        'mail',
        'sicpro_app_administracion',
    ],
    "data":  [
      'security/ir.model.access.csv',
      'data/mail_template.xml',
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
      'wizards/backup_custom_message_wizard_view.xml',
      'wizards/backup_deletion_confirmation_view.xml',
      'views/backup_remote_server.xml',
      'views/backup_local.xml',
      'views/menuitems.xml',
  ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
