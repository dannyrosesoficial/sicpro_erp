# -*- coding: utf-8 -*-

{
    'name': 'SICPRO - Edición Masiva',
    'version': '1.0',
    'summary': """Edición masiva de datos""",
    'description': """Este módulo se encarga de la edición en masa de todos los modelos de datos""",
    'category': 'Herramientas',
    'author': 'Daniel Barrero Reyes',
    'website': "https://www.facebook.com/daniel.barrero.1253",
    'license': 'AGPL-3',
    'sequence': 3,

    'uninstall_hook': 'uninstall_hook',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/mass_editing_view.xml',
    ],
    "installable": True,
    'application': True,
}
