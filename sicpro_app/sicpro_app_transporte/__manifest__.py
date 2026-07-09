# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Transporte',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Transporte',
    'summary': "Esta aplicación se encargará de todo el control del parque "
               "automotor de la división.",
    'description': "Esta aplicación se encargará de todo el control del parque "
               "automotor de la división.",
    'depends': [
        'base',
        'mail',
        'sicpro_modulo_nomencladores',
        'sicpro_app_trabajadores',
        'sicpro_modulo_widget_contador',
        'sicpro_app_administracion',
    ],
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'license': 'AGPL-3',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sicpro_app_transporte_modelo.xml',
        'data/sicpro_app_transporte_estado.xml',
        'data/mail_template.xml',
        'informes/informe_modelo_m1.xml',
        'informes/informe_costo_piquera.xml',
        'views/transporte_modelo_views.xml',
        'views/transporte_views.xml',
        'views/transporte_distancias_views.xml',
        'views/transporte_combustible_views.xml',
        'views/transporte_estado_views.xml',
        'views/transporte_trabajadores.xml',
        'views/transporte_piquera_view.xml',
        'views/transporte_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
        'web.report_assets_common': [
            'sicpro_app_transporte/static/src/css/informe_modelo_m1.scss',
            'sicpro_app_transporte/static/src/css/informe_costo_piquera.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
