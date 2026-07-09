# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Nomenclador del sindicato',
    'version': '19.0.0.0.1',
    'sequence': 3,
    'category': 'Administración',
    'summary': "Este módulo agrega todas las bases del nomenclador de las "
               "secciones sindicales de la DVPE",
    'description': "Este módulo agrega todas las bases del nomenclador de las "
                   "secciones sindicales de la DVPE",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'license': 'AGPL-3',
    'depends': [
                'base',
                'sicpro_app_administracion',
                'sicpro_app_trabajadores',
                'sicpro_modulo_nomencladores',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/sindicato_views.xml',
        'views/trabajadores_areas_views.xml',
        'views/trabajadores_views.xml',
        'views/nomencladores_menu_views.xml'
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
