# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Instrucciones Laborales',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Trabajadores',
    'summary': "Esta aplicación se encargará de todo el control de las "
               "instrucciones que se le realizan a los trabajadores",
    'description': "Esta aplicación se encargará de todo el control de las "
               "instrucciones que se le realizan a los trabajadores",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
        'survey',
        'sicpro_app_trabajadores',
        'sicpro_app_encuestas',
        'sicpro_app_administracion',
                ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/instrucciones_etiquetas_views.xml',
        'views/instrucciones_instruccion_views.xml',
        'views/instrucciones_trabajador_views.xml',
        'views/instrucciones_dashboard_views.xml',
        'data/ir_cron.xml',
        'data/mail_template.xml',
        'informes/informe_modelo_instrucciones_views.xml',
        'views/instrucciones_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_instrucciones/static/src/scss/instrucciones.scss'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
