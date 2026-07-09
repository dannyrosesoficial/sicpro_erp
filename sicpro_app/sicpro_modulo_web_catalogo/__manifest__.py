# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Catálogo Público de Módulos',
    'version': '19.0.0.0.1',
    'summary': "Portal público y transparente del ecosistema de aplicaciones instaladas en SICPRO ERP",
    'description': "Portal público y transparente del ecosistema de aplicaciones instaladas en SICPRO ERP",
    'category': 'Website',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'web',
        'sicpro_modulo_web',
        'sicpro_app_administracion',
    ],
    'data': [
        'views/website_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
