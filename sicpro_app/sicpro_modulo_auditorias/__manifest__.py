# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Registros de Auditoria',
    'version': '19.0.0.0.1',
    'summary': 'Auditoría de acciones y peticiones HTTP',
    'description': 'Auditoría de acciones y peticiones HTTP',
    'category': 'Técnico',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
     'price': 0,
     'currency': 'CUP',
     'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'base',
        'sicpro_app_administracion'
    ],
    'data': [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "views/auditlog_http_request_views.xml",
        "views/auditlog_http_session_views.xml",
        "views/auditlog_log_line_views.xml",
        "views/auditlog_log_views.xml",
        "views/auditlog_rule_views.xml",
        "views/menu.xml",
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
