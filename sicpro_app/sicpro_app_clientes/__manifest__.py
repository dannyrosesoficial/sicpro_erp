# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Clientes',
    'version': '19.0.0.0.1',
    'category': 'Trabajadores',
    'summary': "Esta aplicación le ofrece una vista rápida de su "
               "directorio de clientes, accesible desde su página de inicio.",
    'description': "Esta aplicación le ofrece una vista rápida de su "
                   "directorio de clientes, accesible desde su página de inicio.",
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 2,
    'depends': [
        'base',
        'sicpro_modulo_nomencladores',
        'mail',
        'sicpro_app_contactos',
        'sicpro_app_administracion',
    ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/clientes_views.xml',
        'views/clientes_etiquetas_views.xml',
        'views/res_user.xml',
        'data/sicpro_app_clientes_etiquetas.xml',
        'views/clientes_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
