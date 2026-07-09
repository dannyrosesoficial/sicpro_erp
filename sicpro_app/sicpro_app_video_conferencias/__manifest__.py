# -*- coding: utf-8 -*-
{
    'name': 'SICPRO: Video Conferencias',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'sequence': 2,
    'category': 'Herramientas',
    'summary': "Video Conferencias",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'AGPL-3',
    'description': "Esta aplicación se encarga de la gestión y programación"
                   " de las videoconferencias mediante la plataforma "
                   "de JITSI-ETECSA",
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
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
    ], 'assets': {'web.assets_backend': [], 'web.qunit_suite_tests': [],
    'web.assets_qweb': [], },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}