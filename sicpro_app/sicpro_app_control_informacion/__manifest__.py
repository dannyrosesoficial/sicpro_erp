# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Control de la Información',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Productividad',
    'summary': "Esta aplicación se encarga del control y gestión de las"
               " informaciones que se procesan en la DVPE.",
    'description': "Esta aplicación se encarga del control y gestión de las"
                   " informaciones que se procesan en la DVPE.",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'calendar',
        'sicpro_app_trabajadores',
        'sicpro_app_administracion',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'data/ir_cron.xml',
        'views/control_informacion_areas_views.xml',
        'views/control_informacion_actividades_views.xml',
        'views/control_informacion_actividades_control_view.xml',
        'views/control_informacion_dashboard_view.xml',
        'views/control_informacion_etiquetas_views.xml',
        'views/control_informacion_dias_views.xml',
        'views/control_informacion_motivo_devolucion_views.xml',
        'views/control_informacion_views.xml',
        'informes/dinamica_atividades_evaluacion_view.xml',
        'views/control_informacion_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
