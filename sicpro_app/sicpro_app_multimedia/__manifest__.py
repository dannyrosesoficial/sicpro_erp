# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Almacén Multimedia Centralizado',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Administración',
    'summary': "Gestión centralizada y optimizada de activos multimedia "
               "para todos los módulos de SICPRO.",
    'description': "Gestión centralizada y optimizada de activos multimedia "
                   "para todos los módulos de SICPRO.",
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
                ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/multimedia_tag_views.xml',
        'views/multimedia_asset_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
