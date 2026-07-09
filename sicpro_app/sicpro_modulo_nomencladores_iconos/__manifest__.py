# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
{
    'name': 'SICPRO: Nomenclador de Iconos',
    'version': '19.0.0.0.1',
    'sequence': 3,
    'category': 'Administración',
    'summary': "Este módulo agrega la vista de los nomencladores de iconos",
    'description': "Este módulo agrega la vista de los nomencladores de iconos",
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
                'sicpro_modulo_nomencladores',
                ],
    'data': [
        'security/ir.model.access.csv',
        'data/sicpro_nomenclador_iconos_fa.xml',
        # 'data/iconos_fab_data.xml',
        # 'data/iconos_far_data.xml',
        # 'data/iconos_fas_data.xml',
        'views/iconos_views.xml',
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
