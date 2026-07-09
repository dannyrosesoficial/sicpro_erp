# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Widget Many2One Info',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Muestra lista de búsqueda de un many2one",
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
        'web',
    ],
    'data': [],
    'assets': {
        'web.assets_qweb': [
            'sicpro_modulo_widget_m2o_info/static/src/xml/popover_template.xml',
        ],
        'web.assets_backend': [
            'sicpro_modulo_widget_m2o_info/static/src/scss/m2o_info_widget.scss',

            'sicpro_modulo_widget_m2o_info/static/src/js/form_renderer.js',
            'sicpro_modulo_widget_m2o_info/static/src/js/m2o_info_widget.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
