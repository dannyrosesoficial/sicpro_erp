# -*- coding: utf-8 -*-
{
    'name': 'SICPRO: Video Conferencias',
    'version': '1.0',
    'sequence': 2,
    'category': 'Herramientas',
    'summary': "Video Conferencias",
    'website': 'https://www.facebook.com/danielbarreroreyes.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'license': 'AGPL-3',
    'description': "Esta aplicación se encarga de la gestión y programación"
                   " de las video conferencias mediante la plataforma "
                   "de JITSI-ETECSA",
    'depends': [
        'base',
        'mail',
        'nucleo_sicpro_erp',
        'web',
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/videoconferencias.xml',
        'views/video_conferencias_views.xml',
        'data/url_jitsi_data.xml',
        'data/plantilla_correo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}