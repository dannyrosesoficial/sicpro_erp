# -*- encoding: utf-8 -*-


{
    'name': 'SICPRO: Sistemas',
    'version': '1.0',
    'category': 'Aplicaciones',
    'summary': "Este modulo agrega a todo el sistema campos y vistas para un "
               "correcto funcionamiento de SICPRO ERP",
    'author': 'Daniel Barrero Reyes',
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'views/res_users_view.xml',
        'views/res_company.xml',
        'data/res_company_data.xml',
    ],
    'installable': True,
    'application': True,
}
