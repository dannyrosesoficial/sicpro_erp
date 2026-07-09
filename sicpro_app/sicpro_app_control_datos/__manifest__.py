# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Control de Datos',
    'version': '1.0',
    'sequence': 2,
    'category': 'Aplicaciones',
    'summary': """Esta aplicación se encargara de todo el control de 
     las tablas del sistema y sobre todo las vistas de las tablas asociadas
     a SICPRO ERP.""",
    'depends': ['base', 'mail', 'sicpro_modulo_nomencladores',
                'sicpro_app_trabajadores', ],
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    'author': 'Daniel Barrero Reyes',
    'license': 'AGPL-3',
    'data': [
        # 'security/contol_datos.xml',
        # 'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
