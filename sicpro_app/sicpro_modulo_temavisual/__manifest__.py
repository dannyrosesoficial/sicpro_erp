# -*- coding: utf-8 -*-


{
    "name": "SICPRO: Tema Visual SICPRO ERP",
    "summary": "Tema para la plataforma SICPRO ERP",
    "version": "1.0",
    "category": "Administración",
    "website": 'https://www.facebook.com/dannyroses.oficial/',
    "description": """Tema Backend para la aplicación SICPRO ERP""",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'LGPL-3',
    'sequence': 3,
    "depends": [
        'base',
        'web',
        'mail',
    ],
    "data": [
        'views/layout.xml',
        'views/res_users.xml',
        'views/res_company.xml',
        'views/web.xml',
        'views/menu_apps_action.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            '/sicpro_modulo_temavisual/static/src/scss/primary_variables_custom.scss',
        ],
        'web._assets_secondary_variables': [
            '/sicpro_modulo_temavisual/static/src/scss/secondary_variables.scss',
        ],
        'web.assets_backend': [
            # se deshabilita algunas funciones internas para dejar por defecto los bordes y color de los botones,
            # bordes de la barra de búsqueda y encabezados
            '/sicpro_modulo_temavisual/static/src/scss/fields_extra_custom.scss',
            ####################################################################################################
            '/sicpro_modulo_temavisual/static/src/scss/layout_style.scss',
            '/sicpro_modulo_temavisual/static/src/scss/sidebar.scss',
            '/sicpro_modulo_temavisual/static/src/scss/chatter.scss',
            '/sicpro_modulo_temavisual/static/src/components/app_menu/menu_order.css',
            '/sicpro_modulo_temavisual/static/src/scss/table.scss',
            '/sicpro_modulo_temavisual/static/src/scss/btn_tema.scss',
            '/sicpro_modulo_temavisual/static/src/scss/menu_items.scss',
            '/sicpro_modulo_temavisual/static/src/scss/dark_mode/theme_accent.scss',
            '/sicpro_modulo_temavisual/static/src/scss/dark_mode/datetimepicker.scss',
            '/sicpro_modulo_temavisual/static/src/scss/dark_mode/theme.scss',
            '/sicpro_modulo_temavisual/static/src/components/app_menu/search_apps.js',
            '/sicpro_modulo_temavisual/static/src/js/tema_clic.js',
            '/sicpro_modulo_temavisual/static/src/js/tema_oscuro.js',
            '/sicpro_modulo_temavisual/static/src/js/ocultar_barra_lateral.js',
            '/sicpro_modulo_temavisual/static/src/js/initial_action_menu_app.js',
            '/sicpro_modulo_temavisual/static/src/js/user_menu.js',
            # amplia el ancho de la vista de formulario
            'sicpro_modulo_temavisual/static/src/scss/formulario_ancho_full.scss',
        ],
        'web.assets_qweb': [
            '/sicpro_modulo_temavisual/static/src/components/app_menu/side_menu.xml',
            '/sicpro_modulo_temavisual/static/src/xml/action_menu_apps.xml',
            # '/sicpro_modulo_temavisual/static/src/xml/boton_modo_oscuro.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}


