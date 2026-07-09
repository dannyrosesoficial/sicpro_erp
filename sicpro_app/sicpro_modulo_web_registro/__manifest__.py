# -*- encoding: utf-8 -*-

{
    'name': 'SICPRO: Web Registro Usuario',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': 'Muestra la página para realizar el registro de usuario al sistema',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": ['nucleo_sicpro_erp',
                "base",
                'sicpro_modulo_web',
                'sicpro_modulo_web_login',
                'sicpro_modulo_plantilla_acceso',
                "sicpro_app_administracion",
                ],
    "data": [
        'security/ir.model.access.csv',
        'templates/registro_template.xml',
        'templates/registro_selector_template.xml',
        'templates/registro_planilla_template.xml',
        'templates/web_template.xml',
        'templates/login_template.xml',
        'templates/registro_terminos_template.xml',
        'views/roles_views.xml',
        'views/registro_roles_views.xml',
        'views/modulo_web_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [],
        'web.web_registros': [
            # Liberia Sweetalert2 para las alertas personalizadas
            'sicpro_modulo_web_registro/static/src/lib/alertas/sweetalert2.min.css',
            'sicpro_modulo_web_registro/static/src/lib/alertas/sweetalert2.all.min.js.js',

            'sicpro_modulo_web_registro/static/src/fonts/material-icon/css/material-design-iconic-font.min.css',
            'sicpro_modulo_web_registro/static/src/css/style.css',
            'sicpro_modulo_web_registro/static/src/js/web_registro_actions.js',
            'sicpro_modulo_web_registro/static/src/vendor/jquery/jquery.min.js',
        ],
        'web.web_registros_planilla': [
            # Liberia Sweetalert2 para las alertas personalizadas
            'sicpro_modulo_web_registro/static/src/lib/alertas/sweetalert2.min.css',
            'sicpro_modulo_web_registro/static/src/lib/alertas/sweetalert2.all.min.js.js',
            # Liberia he para decodificar html
            'sicpro_modulo_web_registro/static/src/lib/he.js',

            'sicpro_modulo_web_registro/static/src/fonts/material-icon/css/font-awesome.min.css',
            'sicpro_modulo_web_registro/static/src/css/bootstrap.min.css',
            'sicpro_modulo_web_registro/static/src/css/style_planilla.css',
            'sicpro_modulo_web_registro/static/src/js/web_registro_actions.js',
            'sicpro_modulo_web_registro/static/src/vendor/jquery/jquery.min2.js',
            'sicpro_modulo_web_registro/static/src/vendor/jquery/bootstrap.min.js',
            'sicpro_modulo_web_registro/static/src/js/script.js',
        ],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}