# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Transferencias de Gastos',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Producción',
    'summary': "Esta aplicación se encarga de gestión y control de las"
               " transferencias de gastos generados por los procesos claves "
               "de la ejecución.",
    'description': "Esta aplicación se encarga de gestión y control de las"
                   " transferencias de gastos generados por los procesos "
                   "claves de la ejecución.",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'AGPL-3',
    'depends': [
        'sicpro_app_administracion',
        'base',
        'calendar',
        'sicpro_app_clientes',
        'sicpro_app_solicitudes',
        'sicpro_app_ordenes_trabajo',
        'sicpro_modulo_widget_buscador_one2many',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/transferencias_ordenes_views.xml',
        'wizard/transferencias_ajustes_views.xml',
        'wizard/transferencias_certificar_views.xml',
        'wizard/transferencias_gastos_cj74_views.xml',
        'wizard/transferencias_ordenes_rechazo_views.xml',
        'views/transferencias_ajustes_historial_views.xml',
        'views/transferencias_cuentas_gastos_views.xml',
        'views/transferencias_gastos_importar_views.xml',
        'views/transferencias_gastos_views.xml',
        'views/transferencias_ordenes_gastos_views.xml',
        'views/transferencias_ordenes_estados_views.xml',
        'views/transferencias_ordenes_morosidad_views.xml',
        'informes/dinamica_periodo_clase_coste_view.xml',
        'informes/dinamica_contabilizado_view.xml',
        'informes/dinamica_pendiente_contabilizar_view.xml',
        'informes/dinamica_pendiente_procesos_view.xml',
        'informes/informe_modelo_transferencia_gastos.xml',
        'views/ordenes_trabajo_views.xml',
        'data/mail_template.xml',
        'data/sicpro_app_transferencias_gastos_ordenes_estados.xml',
        'data/sicpro_app_transferencias_cuentas_gastos.xml',
        'data/sicpro_app_transferencias_gastos_ordenes_morosidad.xml',
        'data/ir_cron.xml',
        'views/transferencias_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_transferencias_gastos/static/src/js/transferir_subir_gastos_cj74.js',
            'sicpro_app_transferencias_gastos/static/src/js/certificar_gastos_cj74.js',
            'sicpro_app_transferencias_gastos/static/src/xml/transferir_subir_gastos_cj74.xml',
            'sicpro_app_transferencias_gastos/static/src/xml/certificar_gastos_cj74.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
