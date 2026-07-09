# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Administrar Certificados Digitales',
    'version': '19.0.0.0.1',
    'summary': "Controla los certificados digitales utilizados por el sistema SICPRO ERP",
    'description': "Controla los certificados digitales utilizados por el sistema",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    'external_dependencies': {'python': ['pyOpenSSL'], },
    'depends': [
        'base',
        'sicpro_app_administracion',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/certificados_digitales_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
