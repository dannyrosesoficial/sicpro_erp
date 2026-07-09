# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: DB-Master Explorer',
    'version': '19.0.0.0.1',
    'category': 'Administración',
    'summary': "Gestión dinámica y edición de tablas crudas con seguridad de doble factor.",
    'description': "Herramienta de administración avanzada para visualizar y "
                   "editar cualquier tabla del sistema dinámicamente. "
                   "Incluye bloqueo de seguridad por contraseña maestra.",
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 2,
    'depends': [
        'base',
        'sicpro_app_administracion',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/security_config_data.xml',
        'data/table_blacklist_data.xml',
        'wizard/master_password_wizard_views.xml',
        'views/db_explorer_views.xml',
        'views/db_audit_log_views.xml',
        'views/menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_db_explorer/static/src/css/explorer_style.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
