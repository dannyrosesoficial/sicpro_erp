# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Multiples Fechas',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Permite la selección de multiples fechas en un solo campo y modificar la tradución de los"
               " meses, semanas y días del formato de calendario.",
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
    ],
    'data': [],
    'assets': {
        'web.assets_backend': {
            '/sicpro_modulo_widget_datepicker/static/src/css/datepicker_widget.css',
            '/sicpro_modulo_widget_datepicker/static/src/js/lib/bootstrap-datepicker.min.js',
            '/sicpro_modulo_widget_datepicker/static/src/js/datepicker_widget.js',
        },
        'web.assets_qweb': {
            '/sicpro_modulo_widget_datepicker/static/src/xml/datepicker_widget.xml',
        },
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
