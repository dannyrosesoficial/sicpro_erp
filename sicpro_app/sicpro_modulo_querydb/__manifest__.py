# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Base de Datos Query',
    'version': '1.0',
    'category': 'Administración',
    'summary': 'Permite el acceso a las bases de datos postgresql mediantes '
               'consulta query',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": ['nucleo_sicpro_erp', 'base', "sicpro_app_administracion"],
    'data': [
            #'security/security.xml',
            'security/ir.model.access.csv',
            'views/query_deluxe_views.xml',
            'wizard/pdforientation.xml',
            'report/print_pdf.xml',
            'data/data.xml'
            ],

    "installable": True,
    'application': True,
    "auto_install": False,
}