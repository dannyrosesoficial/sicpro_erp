# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Encuestas',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Productividad',
    'summary': "Esta aplicación se encargará de todo el control de las"
               " encuestas y pruebas creadas por los usuarios.",
    'description': "Esta aplicación se encargará de todo el control de las"
               " encuestas y pruebas creadas por los usuarios.",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'license': 'AGPL-3',
    'depends': ['base',
                'survey',
                'sicpro_app_trabajadores',
                'sicpro_app_administracion',
                ],
    'data': [
        'views/survey_templates.xml',
        'views/survey_user_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
