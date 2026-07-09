# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    'name': 'SICPRO: Actividades',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Productividad',
    'summary': "Esta aplicación se encargará de la gestión y productividad"
               " mediantes tareas y notas.",
    'description': "Esta aplicación se encargará de la gestión y productividad"
                   " mediantes tareas y notas.",
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
        'project',
        'project_todo',
                ],
    'data': [
        'views/actividades_menu_views.xml'
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}


