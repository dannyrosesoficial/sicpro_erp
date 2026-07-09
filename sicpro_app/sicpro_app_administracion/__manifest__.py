# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Administración',
    'version': '19.0.0.0.1',
    'summary': "Aplicación para la administración de SICPRO ERP",
    'description': "Aplicación para la administración de SICPRO ERP",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 1,
    'external_dependencies':
        {
            'python': ['python-ldap'],
            'apt': {'python-ldap': 'python3-ldap',},
    },
    'depends': [
        'base',
        'mail',
        'web',
        'calendar',
        'base_automation',
        'base_import',
        'auth_ldap',
        'bus',
        'sicpro_modulo_roles',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/res_company.xml',
        'data/mail_channel.xml',
        'data/res_user.xml',
        'data/ir_mail_server.xml',
        'data/mail_template.xml',
        'data/ir_cron.xml',
        'data/ir_config_parameter.xml',
        'views/res_users_view.xml',
        'views/ir_module_view.xml',
        'views/res_company.xml',
        'views/webclient_templates.xml',
        'views/sicpro_app_administracion.xml',
        'views/administracion_menus_accesos_view.xml',
        'views/administracion_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_administracion/static/src/css/web_administracion.scss',
            'sicpro_app_administracion/static/src/js/import_menu_patch.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
