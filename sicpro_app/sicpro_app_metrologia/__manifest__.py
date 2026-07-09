# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Metrología',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Servicios de Apoyo',
    'summary': "Esta aplicación se encargará de todo el control de los "
               "instrumentos de medición de la división.",
    'description': "Esta aplicación se encargará de todo el control de los "
               "instrumentos de medición de la división.",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'license': 'AGPL-3',
    'depends': ['base',
                'mail',
                'sicpro_app_administracion',
                'sicpro_modulo_nomencladores',
                'sicpro_app_trabajadores',
                ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/mail_template.xml',
        'data/sicpro_app_metrologia_centro_calibracion.xml',
        'data/sicpro_app_metrologia_estado_tecnico.xml',
        'views/mail_activity_views.xml',
        'views/metrologia_estado_tecnico_views.xml',
        'views/metrologia_equipos_procesos_views.xml',
        'views/metrologia_centro_calibracion_views.xml',
        'views/metrologia_magnitudes_views.xml',
        'views/metrologia_equipamientos_views.xml',
        'views/metrologia_plan_calibracion_views.xml',
        'views/metrologia_todos_equipos_views.xml',
        'views/metrologia_registro_magnitudes_views.xml',
        'views/metrologia_trabajadores_views.xml',
        'views/metrologia_dashboard_equipos_views.xml',
        'views/metrologia_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_metrologia/static/src/scss/maintenance_team_dashboard.scss'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
