# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Base de Datos Query',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': 'Permite el acceso a las bases de datos PostgreSQL mediantes consulta query',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
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
    "pre_init_hook": "pre_init_check",
}