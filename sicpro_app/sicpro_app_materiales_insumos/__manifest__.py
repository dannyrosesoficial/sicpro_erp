# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Materiales e Insumos',
    'version': '19.0.0.0.1',
    'category': 'Producción',
    'summary': "Esta aplicación le ofrece un control de los "
               "Materiales e Insumos que se utilizan en los procesos.",
    'description': "Esta aplicación le ofrece un control de los "
               "Materiales e Insumos que se utilizan en los procesos.",
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
 'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 2,
    'depends': [
        'sicpro_app_administracion',
        'base',
        'mail',
        'sicpro_modulo_nomencladores',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sicpro_app_materiales_insumos_etiquetas.xml',
        'data/sicpro_app_materiales_insumos_um.xml',
        'views/productos_materiales_insumos_views.xml',
        'views/productos_etiquetas_views.xml',
        'views/productos_um_views.xml',
        'views/productos_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
