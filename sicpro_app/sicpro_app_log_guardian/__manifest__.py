# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Log Guardian',
    'version': '19.0.0.0.1',
    'category': 'Administración',
    'summary': "Gestión centralizada de Logs, monitorización y ciclo de vida de errores.",
    'description': "Módulo avanzado para la lectura, monitorización y gestión"
                   " de resoluciones de archivos de Log "
                   "(Odoo, Nginx, PostgreSQL) integrando detecciones de"
                   " anomalías y alertas en tiempo real para el ecosistema SICPRO.",
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
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/severity_mappings_data.xml',
        'data/anomaly_detection_rules.xml',
        'data/log_sources_data.xml',
        'data/retention_rules_data.xml',
        'data/email_templates_data.xml',
        'views/log_config_views.xml',
        'views/log_record_views.xml',
        'views/menus.xml',
        'report/log_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_log_guardian/static/src/css/log_styles.css',
        ],
               },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}