# -*- encoding: utf-8 -*-
{
    'name': 'SICPRO: Modificación Vistas de Lista',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'summary': "Modifica las vistas listas",
    'description': "Este módulo se encarga de todas las modificaciones a las vistas de árbol o lista",
    'category': 'Administración',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': "https://www.facebook.com/dannyroses.oficial/",
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        'nucleo_sicpro_erp',
        'base',
        'web'
    ],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'sicpro_modulo_vistas/static/src/scss/list_form_view.scss',
            'sicpro_modulo_vistas/static/src/js/list_view.js',
            'sicpro_modulo_vistas/static/src/js/record_highlight.js',
            'sicpro_modulo_vistas/static/src/scss/kanban_view.scss'
        ],
        "web.assets_qweb": [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
