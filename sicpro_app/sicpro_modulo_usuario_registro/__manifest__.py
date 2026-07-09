# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Registros de Usuario',
    'version': '19.0.0.0.1',
    'summary': "Detalles del usuario de inicio de sesión y dirección IP",
    'description': "Este módulo registra la información de inicio de sesión"
                   " del usuario",
    'category': 'Técnico',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'base',
        'web',
        'sicpro_app_administracion'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'wizard/pass_user_backup_wizard_views.xml',
        'views/registro_usuarios_reporte.xml',
        'views/registro_usuarios_reporte_template.xml',
        'views/registro_usuarios_reporte_wizard.xml',
        'views/registro_usuarios_views.xml',
        'views/registro_ips_view.xml',
        'views/res_user_views.xml',
        ],
    'assets':
        {
            'web.assets_backend': [],
        },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
