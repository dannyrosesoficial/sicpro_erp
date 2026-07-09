# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Base de Datos Query',
    'version': '19.0.0.1',
    'category': 'Administración',
    'summary': 'Permite el acceso a las bases de datos PostgreSQL'
               ' mediantes consulta query',
    'description': 'Permite el acceso a las bases de datos PostgreSQL'
                   ' mediantes consulta query',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        'base',
        "mail",
        "sicpro_app_administracion"
    ],
    'data': [
            'security/security.xml',
            'security/ir.model.access.csv',
        'data/querydeluxe.xml',
            'views/querydeluxe.xml',
            'wizard/pdforientation.xml',
            'report/print_pdf.xml',
            ],

    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}