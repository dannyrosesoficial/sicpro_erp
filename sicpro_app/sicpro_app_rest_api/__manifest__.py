# -*- encoding: utf-8 -*-


{
    'name': 'SICPRO: API Rest',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    'estado': 'Desarrollo',
    'category': 'Administración',
    'summary': 'Permite la conexión con SICPRO ERP mediante API Rest',
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
        "base",
    ],
    "data": [
        'security/api.xml',
        'security/ir.model.access.csv',
        # Views
        'views/api_rest_version_views.xml',
        'views/api_rest_path_views.xml',
        'views/api_rest_tag_views.xml',
        'views/api_rest_log_views.xml',
        'views/api_rest_historial_views.xml',
        'views/swagger_templates.xml',
        'views/api_rest_menu_views.xml',
    ],
    'assets': {
        'sicpro_app_rest_api.assets_swagger': [
            'sicpro_app_rest_api/static/lib/swagger-ui-3.38.0/swagger-ui.css',
            'sicpro_app_rest_api/static/lib/swagger-ui-3.38.0/swagger-ui-bundle.js',
            'sicpro_app_rest_api/static/lib/swagger-ui-3.38.0/swagger-ui-standalone-preset.js',
        ],
    },
    "test": [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
