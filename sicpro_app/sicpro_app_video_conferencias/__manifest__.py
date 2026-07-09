# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
{
    'name': 'SICPRO: Video Conferencias',
    'version': '19.0.0.0.1',
    'sequence': 2,
    'category': 'Productividad',
    'summary': "Esta aplicación se encarga de la gestión y programación"
                   " de las videoconferencias mediante la plataforma "
                   "de JITSI-ETECSA",
    'description': "Esta aplicación se encarga de la gestión y programación"
                   " de las videoconferencias mediante la plataforma "
                   "de JITSI-ETECSA",
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
        'mail',
        'web',
        'sicpro_app_administracion',
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/video_conferencias_views.xml',
        'data/ir_config_parameter.xml',
        'data/mail_template".xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
