# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Marcadores',
    'version': '19.0.0.0.1',
    'summary': "Crea pestaña de marcadores para agregar las vistas más "
               "utilizadas en la barra de tareas.",
    'description': "Crea pestaña de marcadores para agregar las vistas más "
                   "utilizadas en la barra de tareas.",
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
     'price': 0,
     'currency': 'CUP',
     'company': 'División de Proyectos y Ejecución de Obras',
     'category': 'Técnico',
     'website': 'https://www.facebook.com/dannyroses.oficial/',
     'license': 'LGPL-3',
     'sequence': 3,
    'depends': [
        'web',
        'sicpro_app_administracion',
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/menu_bookmark_views.xml",
        "views/res_config_setting_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sicpro_modulo_marcadores/static/src/components/add_bookmark/add_bookmark.js",
            "sicpro_modulo_marcadores/static/src/components/add_bookmark/add_bookmark.xml",
            "sicpro_modulo_marcadores/static/src/components/bookmark/bookmark.js",
            "sicpro_modulo_marcadores/static/src/components/bookmark/bookmark.xml",
            "sicpro_modulo_marcadores/static/src/components/widget_announcement/widget_announcement.scss",
            "sicpro_modulo_marcadores/static/src/components/widget_announcement/widget_announcement.js",
            "sicpro_modulo_marcadores/static/src/components/widget_announcement/widget_announcement.xml",
            "sicpro_modulo_marcadores/static/src/components/widget_hour/widget_hour.scss",
            "sicpro_modulo_marcadores/static/src/components/widget_hour/widget_hour.js",
            "sicpro_modulo_marcadores/static/src/components/widget_hour/widget_hour.xml",
        ],
    },
     'installable': True,
     'application': True,
     'auto_install': False,
     'pre_init_hook': 'pre_init_check',
}
