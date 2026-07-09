# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    'name': 'SICPRO: Actualizar vistas',
    'version': '19.0.0.0.1',
    'category': 'Técnico',
    'summary': 'Actualizar automáticamente vistas de lista o kanban',
    'description': 'Active el botón de actualización automática para recargar la vista cada'
                   '30 segundos. La actualización recargará y actualizará los datos de la vista.',
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
        "base",
        "web",
        'sicpro_app_administracion',
    ],
    "data": [],
    'assets': {
        'web.assets_backend': [
            (
                'after',
                '/web/static/src/search/control_panel/control_panel.js',
                '/sicpro_modulo_tema_auto_actualizar/static/src/search/control_panel.js',
            ),
            (
                'after',
                '/web/static/src/search/control_panel/control_panel.xml',
                '/sicpro_modulo_tema_auto_actualizar/static/src/search/control_panel.xml',
            ),
        ],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}