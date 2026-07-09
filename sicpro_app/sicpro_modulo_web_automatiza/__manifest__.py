# -*- coding: utf-8 -*-


{
    'name': 'SICPRO: Web Automatización de Correos',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': 'Se encarga de gestionar y mostrar los nomencladores de asuntos de los correos de entrada en la pagina '
               'principal del sistema.',
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
        'sicpro_modulo_web_login',
        'sicpro_modulo_base_correos_entrantes',
        'sicpro_modulo_dashboard_extendido',
    ],
    "data": [
        'security/ir.model.access.csv',
        'templates/automatiza_templates.xml',
        'templates/web_templates.xml',
        'view/automatiza_views.xml',
        'view/automatiza_menu_views.xml'
            ],
    'assets': {
        'web.assets_backend': [],
        'web.web_automatizacion': [
            'sicpro_modulo_web_automatiza/static/src/vendor/animate.css/animate.min.css',
            'sicpro_modulo_web_automatiza/static/src/vendor/aos/aos.css',
            'sicpro_modulo_web_automatiza/static/src/vendor/bootstrap/css/bootstrap.min.css',
            'sicpro_modulo_web_automatiza/static/src/vendor/bootstrap-icons/bootstrap-icons.css',
            'sicpro_modulo_web_automatiza/static/src/vendor/boxicons/css/boxicons.min.css',
            'sicpro_modulo_web_automatiza/static/src/vendor/glightbox/css/glightbox.min.css',
            'sicpro_modulo_web_automatiza/static/src/vendor/remixicon/remixicon.css',
            'sicpro_modulo_web_automatiza/static/src/vendor/swiper/swiper-bundle.min.css',
            'sicpro_modulo_web_automatiza/static/src/css/style.css',

            'sicpro_modulo_web_automatiza/static/src/vendor/aos/aos.js',
            'sicpro_modulo_web_automatiza/static/src/vendor/bootstrap/js/bootstrap.bundle.min.js',
            'sicpro_modulo_web_automatiza/static/src/vendor/glightbox/js/glightbox.min.js',
            'sicpro_modulo_web_automatiza/static/src/vendor/isotope-layout/isotope.pkgd.min.js',
            'sicpro_modulo_web_automatiza/static/src/vendor/swiper/swiper-bundle.min.js',
            'sicpro_modulo_web_automatiza/static/src/js/main.js',
        ],
        'web.web_automatizacion_js': [
            'sicpro_modulo_web_automatiza/static/src/vendor/aos/aos.js',
            'sicpro_modulo_web_automatiza/static/src/vendor/bootstrap/js/bootstrap.bundle.min.js',
            'sicpro_modulo_web_automatiza/static/src/vendor/glightbox/js/glightbox.min.js',
            'sicpro_modulo_web_automatiza/static/src/vendor/isotope-layout/isotope.pkgd.min.js',
            'sicpro_modulo_web_automatiza/static/src/vendor/swiper/swiper-bundle.min.js',
            'sicpro_modulo_web_automatiza/static/src/js/main.js',
        ],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}
