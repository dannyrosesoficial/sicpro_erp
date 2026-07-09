# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: API Conector (SIPETC)',
    'version': '19.0.0.0.1',
    'category': 'Técnico',
    'summary': "Este módulo se encarga de generar la configuración para la "
               "conexión de la aplicación de Transporte",
    'description': "Este módulo se encarga de generar la configuración para la "
               "conexión de la aplicación de Transporte",
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
                'base',
                'sicpro_app_administracion',
                'sicpro_app_transporte',
                'sicpro_app_trabajadores',
                'sicpro_modulo_api_conector',
                ],
    'data': [
        'data/ir_cron.xml',
        'data/mail_template.xml',
        'views/conector_rest_api_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
