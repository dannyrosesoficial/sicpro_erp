# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Contactos',
    'version': '19.0.0.0.1',
    'summary': "Visualización de los contactos del sistema",
    'description': "Visualización de los contactos del sistema",
    'category': 'Trabajadores',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'contacts',
        'base', 'mail',
        'sicpro_app_administracion',
        'sicpro_app_trabajadores',
    ],
    "data": [
        'views/contactos_trabajadores_views.xml',
        'views/contactos_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
