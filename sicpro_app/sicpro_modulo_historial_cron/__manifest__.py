# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Historial de Ejecución Cron',
    'version': '19.0.0.0.1',
    'summary': "Registra historial de ejecuciones de cron y envía alertas"
               " a roles configurados.",
    'description': "Registra historial de ejecuciones de cron y envía alertas"
                   " a roles configurados.",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
        'sicpro_app_administracion',
    ],
    "data": [
        'data/mail_template.xml',
        'security/ir.model.access.csv',
        'views/ir_cron_views.xml',
        'views/ir_cron_history_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
        'web.assets_qweb': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
