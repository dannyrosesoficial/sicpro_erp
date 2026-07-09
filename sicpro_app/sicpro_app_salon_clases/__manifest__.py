# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Salón de Clases',
    'version': '19.0.0.0.1',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'category': 'Documentos',
    'sequence': 2,
    'summary': "Esta aplicación se encargara de la preparación de los usuarios"
               " mediante de diversos temas de interés de trabajo.",
    'description': "Esta aplicación se encargara de la preparación de los usuarios"
               " mediante de diversos temas de interés de trabajo.",
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'AGPL-3',
    'depends': [
        'web',
        'base',
        'sicpro_app_administracion',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/salon_clases_etiquetas_views.xml',
        'views/salon_clases_tipo_views.xml',
        'views/salon_clases_views.xml',
        'views/salon_clases_temas_views.xml',
        'views/salon_clases_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',

}
