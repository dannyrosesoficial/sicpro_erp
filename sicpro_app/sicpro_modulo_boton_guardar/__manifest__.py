# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Botón Guardar',
    'version': '19.0.0.0.1',
    'summary': "Agrega el botón de guardar y cancelar a todas las vistas del sistema",
    'description': "Agrega el botón de guardar y cancelar a todas las vistas del sistema",
    'category': 'Técnico',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    'depends': [
        'base',
        'web',
        'sicpro_app_administracion',
    ],
    'data': [ ],
    'assets': {
        'web.assets_backend':
            [
                'sicpro_modulo_boton_guardar/static/src/**/*',
            ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
