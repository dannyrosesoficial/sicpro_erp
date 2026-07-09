# -*- encoding: utf-8 -*-
{
    'name': 'SICPRO: Numeración de Lista',
    'version': '1.0',
    'summary': "Numera los datos de la vista lista",
    'description': "Este módulo se encarga de autoenumerar los datos de las "
                   "vistas de árbol o tree",
    'category': 'Herramientas',
    'author': 'Daniel Barrero Reyes',
    'website': "https://www.facebook.com/daniel.barrero.1253",
    'license': 'AGPL-3',
    'sequence': 3,

    "depends": ['web'],
    'data': [
             'views/listview_templates.xml',
             ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
