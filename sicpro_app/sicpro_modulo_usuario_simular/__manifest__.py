# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    "name": "SICPRO: Simulación de Usuarios",
    'version': '19.0.0.0.1',
    "category": "Técnico",
    "summary": "Aplicación para simulación de sesión",
    "description": "Aplicación para simulación de sesión de los usuarios",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": [
        "base",
        "web",
        'sicpro_app_administracion'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/user_selection_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_modulo_usuario_simular/static/src/js/systray_button.js',
            'sicpro_modulo_usuario_simular/static/src/xml/systray_button_templates.xml',
        ]},
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}

