# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


{
    'name': 'SICPRO: Registro/Soporte/Bitácora',
    'version': '19.0.0.1',
    'category': 'Técnico',
    'summary': 'El módulo se encarga de actualizar los tickets de soporte'
               ' y la bitácora del usuario',
    'description': 'El módulo se encarga de actualizar los tickets de soporte'
                   ' y la bitácora del usuario',
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
        'sicpro_app_administracion',
        'sicpro_modulo_roles',
        'sicpro_modulo_web_registro',
        'sicpro_app_soporte',
    ],
    "data": [
        'view/solicitud_bitacora_views.xml',
        'view/solicitud_roles_views.xml',
        'view/solicitud_soporte_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
}
