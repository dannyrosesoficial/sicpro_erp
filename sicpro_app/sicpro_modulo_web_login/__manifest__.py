# -*- encoding: utf-8 -*-

{
    'name': 'SICPRO: Web Login SICPRO ERP',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': 'Crear una nueva configuración del login para SICPRO ERP',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'license': 'AGPL-3',
    'sequence': 3,
    "depends": ['nucleo_sicpro_erp', "base",
                'base_setup', 'web',
                'social_media',
                'sicpro_modulo_web',
                'sicpro_modulo_usuario_registro',
                "sicpro_app_administracion",
                ],
    "data": [
        'templates/login_template.xml',
        'data/ir_config_parameter.xml',
    ],
    'assets': {
        'web.web_login': [
            'sicpro_modulo_web_login/static/src/css/bootstrap.min.css',
            'sicpro_modulo_web_login/static/src/css/owl.carousel.min.css',
            'sicpro_modulo_web_login/static/src/fonts/icomoon/style.css',
            'sicpro_modulo_web_login/static/src/css/style.css',
        ],
    },
    "installable": True,
    'application': True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}