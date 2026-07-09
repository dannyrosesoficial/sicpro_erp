# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Cuadro de Mando Integral',
    'version': '19.0.0.0.1',
    'category': 'Producción',
    'summary': "La aplicación se encarga de la gestión del CMI de la DVPE.",
    'description': "La aplicación se encarga de la gestión del CMI de la DVPE.",
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
        'mail',
        'sicpro_app_administracion',
        'sicpro_modulo_nomencladores',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/cmi_acciones_estados_views.xml',
        'views/cmi_acciones_modo_control_views.xml',
        'views/cmi_indicadores_cambios_views.xml',
        'views/cmi_indicadores_acciones_views.xml',
        'views/cmi_indicadores_views.xml',
        'views/cmi_objetivos_anuales_views.xml',
        'views/cmi_objetivos_estrategicos_views.xml',
        'views/cmi_perspectivas_views.xml',
        'views/cmi_perspectivas_eje_estrategico_views.xml',
        'views/cmi_perspectivas_periodo_views.xml',
        'views/cmi_perspectivas_anios_views.xml',
        'report/indicadores_report_views.xml',
        'data/mail_template.xml',
        'data/sicpro_app_cmi_acciones_estado.xml',
        'data/ir_cron.xml',
        'data/sicpro_app_cmi_perspectivas_periodos.xml',
        'informes/cmi_reporte_wizard.xml',
        'informes/cmi_reporte_template_completo.xml',
        'informes/cmi_reporte_template_ejes.xml',
        'informes/cmi_reporte_template_acciones.xml',
        'views/cmi_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_cmi/static/src/scss/dashboard.scss',
        ],
               },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
