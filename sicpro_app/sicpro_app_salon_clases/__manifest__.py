# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Salón de Clases',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'category': 'Productividad',
    'sequence': 2,
    'summary': "Esta aplicación se encargara de la preparación de los usuarios"
               " mediante de diversos temas de interés."
               " del trabajo.",
    'description': "Modulo de Salón de clases",
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'AGPL-3',
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'web',
        'base',
        'mail',
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
    ],
    'data': [
        'security/salon_clases.xml',
        'security/ir.model.access.csv',
        'views/salon_clases_etiquetas_views.xml',
        'views/salon_clases_tipo_views.xml',
        'views/salon_clases_views.xml',
        'views/salon_clases_temas_views.xml',
        'data/ir_config_parameter_data.xml',
        'data/ir_cron_data.xml',
        'views/salon_clases_menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_salon_clases/static/src/js/many_2_many_salon.js',
        ],
        'web.qunit_suite_tests': [],
        'web.assets_qweb': [
            'sicpro_app_salon_clases/static/src/xml/base.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
