# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Vistas de los modelos de datos',
    'version': '19.0.0.0.1',
    'category': 'Técnico',
    'summary': "Este módulo permite la consulta de vistas dinámicas a los"
               " modelos de datos",
    'description': "Este módulo permite la consulta de vistas dinámicas a los"
                   " modelos de datos",
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'sicpro_app_administracion',
        'base',    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/modelos_vistas_views.xml',
        'views/ir_model_view.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
