# -*- coding: utf-8 -*-

{
    "name": "Dependencia para sicpro_modulo_temavisual",
    "summary": "Dependencia para sicpro_modulo_temavisual.",
    "version": "1.0",
    "category": "Aplicaciones",
    'author': 'Daniel Barrero Reyes',
    'website': 'https://www.facebook.com/daniel.barrero.1253',
    "license": "LGPL-3",
    "installable": True,
    "depends": ['web','mail',],
    "data": [
        'views/assets.xml',
        'views/res_users.xml',
        'views/web.xml',
    ],
    'qweb': [
        'static/src/xml/apps.xml',
        'static/src/xml/form_view.xml',
        'static/src/xml/navbar.xml',
    ],
}
