# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    'name': 'SICPRO: Calendario',
    'version': '19.0.0.0.1',
    'summary': "Aplicación para la gestión de calendario de SICPRO ERP",
    'description': "Aplicación para la gestión de calendario de SICPRO ERP",
    'category': 'Productividad',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'web',
        'calendar',
        'sicpro_modulo_nomencladores',
        'sicpro_app_trabajadores',
        'sicpro_app_reuniones',
        'sicpro_app_administracion',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'data/ir_cron.xml',
        'informes/calendar_reporte_individual_template.xml',
        'informes/calendar_reporte_dvpe_template.xml',
        'informes/calendar_reporte_cumplimiento_template.xml',
        'views/calendar_reporte_plan_wizard.xml',
        'views/calendar_reporte_cumplimiento_wizard.xml',
        'views/calendar_tipo_calendario_views.xml',
        'views/calendar_views.xml',
        'views/calendar_actividades_organizativas_views.xml',
        'views/calendar_cargos_externos_views.xml',
        'views/calendar_pie_firma_views.xml',
        'views/calendar_tareas_principales_generales_views.xml',
        'views/calendar_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
