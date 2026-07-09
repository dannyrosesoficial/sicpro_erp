# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Formato a Fechas',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Permite agregar nuevo estilo de formato a las fechas",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'nucleo_sicpro_erp',
        'base',
        'web',
    ],
    'data': [],
    'assets': {
        'web.assets_qweb': [
            'sicpro_modulo_widget_time_delta/static/src/xml/*.xml',
        ],
        'web.assets_backend': [
            'sicpro_modulo_widget_time_delta/static/src/css/widget.css',
            'sicpro_modulo_widget_time_delta/static/src/lib/duration-picker/jquery-duration-picker.css',
            'sicpro_modulo_widget_time_delta/static/src/js/widget.js',
            'sicpro_modulo_widget_time_delta/static/src/lib/duration-humanize/humanize-duration.js',
            'sicpro_modulo_widget_time_delta/static/src/lib/duration-picker/jquery-duration-picker.js'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
