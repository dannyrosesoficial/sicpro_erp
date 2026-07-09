# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

{
    'name': 'SICPRO: Medios Informáticos',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Servicios de Apoyo',
    'summary': "Esta aplicación se encarga del control, gestión de "
               "mantenimiento y destinos finales de los medios informáticos.",
    'description': "Esta aplicación se encarga del control, gestión de"
                   " mantenimiento y destinos finales de los medios informáticos.",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'maintainer': 'Daniel Barrero Reyes / Soporte Técnico SICPRO',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sicpro_app_administracion',
        'sicpro_modulo_nomencladores',
        'sicpro_app_trabajadores',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'data/sicpro_app_medios_informaticos_tramites.xml',
        'data/sicpro_app_medios_informaticos_tipo_equipo.xml',
        'wizard/medios_informaticos_importar_wizard_views.xml',
        'views/medios_informaticos_views.xml',
        'views/medios_informaticos_taller_views.xml',
        'views/medios_informaticos_baja_views.xml',
        'views/medios_informaticos_pendientes_piezas_views.xml',
        'views/medios_informaticos_importar_views.xml',
        'views/medios_informaticos_tipo_equipo_views.xml',
        'views/medios_informaticos_tramites_views.xml',
        'views/medios_informaticos_historial_views.xml',
        'views/medios_informaticos_trabajador_views.xml',
        'views/medios_informaticos_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_medios_informaticos/static/src/xml/importar_medios_informaticos.xml',
            '/sicpro_app_medios_informaticos/static/src/js/importar_medios_informaticos.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    "pre_init_hook": "pre_init_check",
}