# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Backup Server Local y Remoto',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Auto backup del sistema SICPRO ERP en el servidor",
    'description': "Este módulo se encarga de generar las salvas programadas del sistema en el propio servidor",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    'external_dependencies': {'python': ['paramiko', 'dropbox', 'gitpython']},
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        'mail',
        'sicpro_app_administracion',
        'sicpro_modulo_api_conector_gitlab_backup',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/cron_automatizacion.xml',
        'data/plantillas_correo_data.xml',
        'views/backup_server_views.xml',
        'views/backup_server_gitlab_views.xml',
        'views/backup_server_menu_views.xml',
        'wizard/dropbox_authcode_wizard_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
