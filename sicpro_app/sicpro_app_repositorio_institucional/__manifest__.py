# -*- coding: utf-8 -*-

{
    'name': 'SICPRO: Repositorio Institucional',
    'version': '1.0.0',
    # Estados (Desarrollo o Producción) Desarrollo: Store o actualiza Producción: Store avisa de nueva actualización
    #'estado': 'Desarrollo',
    'sequence': 2,
    'category': 'Documentos',
    'summary': "Esta aplicación se encargará de la gestión de la información institucional de la división",
    'website': 'https://www.facebook.com/dannyroses.oficial/',
    'author': 'Daniel Barrero Reyes',
    'support': 'daniel.borrero@etecsa.cu',
    'price': 0,
    'currency': 'CUP',
    'company': 'División de Proyectos y Ejecución de Obras',
    'license': 'AGPL-3',
    'description': "Esta aplicación se encargará de la gestión de la información institucional de la división",
    # 'external_dependencies': {'python': ['nombre del paquete', 'nombre del paquete']},
    'depends': [
        'nucleo_sicpro_erp',
        'sicpro_app_administracion',
        'sicpro_app_trabajadores',
        'base',
        'mail',
    ],
    'data': [
        'security/repositorios_security.xml',
        'security/ir.model.access.csv',
        'data/repositorio_tipos_data.xml',
        'data/repositorio_estados_data.xml',
        'data/repositorio_licencia_data.xml',
        'data/repositorio_facultad_data.xml',
        'views/repositorio_estado_views.xml',
        'views/repositorio_etiquetas_views.xml',
        'views/repositorio_facultad_views.xml',
        'views/repositorio_licencia_views.xml',
        'views/repositorio_tipo_views.xml',
        'views/repositorio_views.xml',
        'views/repositorio_menu_views.xml',
         ],
    'assets': {
        'web.assets_backend': [
            'sicpro_app_repositorio_institucional/static/src/css/repositorio_institucional.scss'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',",

 }
