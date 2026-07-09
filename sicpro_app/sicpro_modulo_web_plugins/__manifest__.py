# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Web Descargas Plugins',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': 'Se encarga de gestionar las descargas de las aplicaciones y plugins de terceros vinculados a SICPRO ERP',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": [
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'base',
        'web',
        'sicpro_modulo_web',
    ],
    "data": [
        'security/ir.model.access.csv',
        'templates/plugins_templates.xml',
        'templates/web_templates.xml',
        'view/plugins_views.xml',
        'view/plugins_menu_views.xml',
            ],
    'assets': {
        'web.assets_backend': [],
        'web.web_plugins': [
            'sicpro_modulo_web_plugins/static/src/vendor/aos/aos.css',
            'sicpro_modulo_web_plugins/static/src/vendor/bootstrap/css/bootstrap.min.css',
            'sicpro_modulo_web_plugins/static/src/vendor/bootstrap-icons/bootstrap-icons.css',
            'sicpro_modulo_web_plugins/static/src/vendor/boxicons/css/boxicons.min.css',
            'sicpro_modulo_web_plugins/static/src/vendor/swiper/swiper-bundle.min.css',
            'sicpro_modulo_web_plugins/static/src/css/style.css',

            'sicpro_modulo_web_plugins/static/src/vendor/aos/aos.js',
            'sicpro_modulo_web_plugins/static/src/vendor/bootstrap/js/bootstrap.bundle.min.js',
            'sicpro_modulo_web_plugins/static/src/vendor/swiper/swiper-bundle.min.js',
            'sicpro_modulo_web_plugins/static/src/vendor/php-email-form/validate.js',
        ],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}
