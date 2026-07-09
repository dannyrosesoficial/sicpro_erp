# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Historial de solicitudes XMLRPC',
    'version': '19.0.0.0.1',
    'summary': 'Se encarga del registro de solicitudes XML-RPC',
    'description': 'Se encarga del registro de solicitudes XML-RPC.',
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'sicpro_app_administracion',
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/xmlrpc_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
