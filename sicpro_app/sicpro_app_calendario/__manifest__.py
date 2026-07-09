# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Calendario',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Aplicación para la gestión de calendario de SICPRO ERP",
    'description': "Aplicación para la gestión de calendario de SICPRO ERP",
    'category': 'Herramientas',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 1,
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'base',
        'web',
        'calendar',
        'nucleo_sicpro_erp',
        'sicpro_modulo_nomencladores',
        'sicpro_app_trabajadores',
        'sicpro_app_reuniones',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        # 'data/calendar_cron.xml', # entra en conflicto con el original del módulo calendar
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
        'web.assets_backend': [
            'sicpro_app_calendario/static/src/js/calendar_count.js',
            'sicpro_app_calendario/static/src/js/calendar_color.js',
        ],
        'web.assets_qweb': [
            'sicpro_app_calendario/static/src/xml/base_calendar.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
